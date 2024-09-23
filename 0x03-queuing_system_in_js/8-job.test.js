import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('Returns an err msg when jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('Invalid_data', queue)).to.throw(
      'Jobs is not an array'
    );
  });

  it('Returns 3 created jobs in the queue when provided with valid job data', () => {
    const jobs = [
      {
	phoneNumber: '4153518780',
	message: 'This is the code 1234 to verify your account',
      },
      {
	phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      },
      {      
        phoneNumber: '4153118782',
        message: 'This is the code 4321 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);
    setTimeout(() => {
      expect(queue.testMode.jobs.length).to.equal(3);

      jobs.forEach((job, idx) => {
        expect(queue.testMode.jobs[idx].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[idx].data).to.deep.equal(job);
      });
      done();
    }, 100);
  });
});
