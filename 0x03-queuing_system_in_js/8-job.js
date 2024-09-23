export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw new Error('Jobs is not an array');

  jobs.forEach((jobDt) => {
    const job = queue.create('push_notification_code_3', jobDt);
    job.save((err) => {
      if (!err) console.log(`Notification job created: ${job.id}`);
    });

    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    job.on('failed', (errMsg) => {
      console.log(`Notification job ${job.id} failed: ${errMsg}`);
    });

    job.on('progress', (prog) => {
      console.log(`Notification job ${job.id} ${prog}% complete`);
    });
});
}
