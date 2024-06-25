import redis from 'redis';
import express from 'express';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);


let reservationEnabled = false;

const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
}

const getCurrentAvailableSeats = async () => {
  const availableSeats = await getAsync('available_seats');
  return availableSeats;
}

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ "numberOfAvailableSeats": availableSeats })
});

app.get('/reserve_seat', async (req, res) => {
    if (reservationEnabled === false) {
        res.json({ "status": "Reservation are blocked" });
        return;
    }
    try {
      const job = queue.create('reserve_seat', {}).save();

      job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
      });

      job.on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
      });

      res.json({ "status": "Reservation in process" });
    } catch (error) {
        res.status(500).json({ "status": "Reservation failed" });
    }
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      done(Error('Not enough seats available'));
      return;
    }
    const newAvailableSeats = Number(availableSeats) - 1;
    await setAsync('available_seats', newAvailableSeats);
    if (newAvailableSeats === 0) {
      reservationEnabled = false;
    }
    if (newAvailableSeats >= 0) {
      done();
      return res.json({ "status": "Queue processing" });
    } else {
      done(Error('Not enough seats available'));
    }
  });
});

app.listen(1245, () => {
  console.log('API available on localhost port 1245');
  reserveSeat(50);
  reservationEnabled = true;
});
