import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool(schoolName, value) {
 client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
  const asyncOp = promisify(client.get).bind(client);
  try {
    const val = await asyncOp(schoolName);
    console.log(val);
  } catch (err) {
    console.log(`Error retrieveing value: ${err}`);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
