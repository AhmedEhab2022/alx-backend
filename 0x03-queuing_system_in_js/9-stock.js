//import redis from 'redis';
//import { promisify } from 'util';
//import express from 'express';

const redis = require('redis');
const express = require('express');
const { promisify } = require('util');

const app = express();
const client = redis.createClient();

client.on('error', (err) => {
  console.error('Redis client error:', err);
});

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5
  }
];

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const getItemById = (id) => listProducts.find((item) => item.itemId === id);

const reserveStockById = async (itemId, stock) => {
  const key = `item.${itemId}`;
  await setAsync(key, stock);
}

const getCurrentReservedStockById = async (itemId) => {
  const key = `item.${itemId}`;
  const currentStock = await getAsync(key);
  return currentStock;
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }
  try {
    const currentStock = await getCurrentReservedStockById(itemId);
    item.currentReservedStock = Number(currentStock) || 0;
    res.json(item);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }
  try {
    const currentStock = await getCurrentReservedStockById(itemId);
    if (currentStock === '0' || !currentStock) {
      res.status(403).json({ status: 'Not enough stock available', id: itemId });
      return;
    }
    const newStock = Number(currentStock) - 1;
    await reserveStockById(itemId, newStock);
    res.json({ status: 'Reservation confirmed', id: itemId });
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(1245, () => {
  console.log('APP available on localhost port 1245');
});
