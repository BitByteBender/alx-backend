import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const host = 'localhost';
const port = 1245;

const client = redis.createClient();
const getCl = promisify(client.get).bind(client);
const setCl = promisify(client.set).bind(client);
const queue = kue.createQueue();

let reservationEnabled = true;

async function reserveSeat(number) {
  await setCl('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getCl('available_seats');
  return parseInt(seats, 10);
}

reserveSeat(50).catch(console.error);

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) return res.json({ status: 'Reservations are blocked' });
  const job = queue.create('reserve_seat').save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });

    return res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errMsg) => {
    console.log(`Seat reservation job ${job.id} failed: ${errMsg.message}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const freeSeats = await getCurrentAvailableSeats();

    if (freeSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    const newSeats = freeSeats - 1;
    await reserveSeat(newSeats);

    if (newSeats === 0) reservationEnabled = false;

    return done();
  });
});

app.listen((port), (host), () => {
  console.log(`Server is listening to ${host}/${port}`);
});
