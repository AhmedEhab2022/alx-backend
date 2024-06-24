import redis from 'redis';

const client = redis.createClient();

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, redis.print);
};

const displaySchoolValue = (schoolName) => {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.log(err);
      return;
    }
    console.log(reply);
  });
};

client.on('connect', () => {
  console.log('Redis client connected to the server');
  displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  displaySchoolValue('HolbertonSanFrancisco');
});

client.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error}`);
});
