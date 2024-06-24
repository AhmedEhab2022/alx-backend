import redis from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
  displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  displaySchoolValue('HolbertonSanFrancisco');
});

client.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error}`);
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, redis.print);
};

const getAsync = promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (error) {
    console.error(error);
  }
};
