import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const host = 'localhost';
const port = 1245;

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

const client = redis.createClient();
const getCl = promisify(client.get).bind(client);
const setCl = promisify(client.set).bind(client);

const getItemById = (id) => {
  return listProducts.find(prd => prd.id === id);
};

app.get('/', (req, res) => res.send('Homepage\n'));
app.get('/list_products', (req, res) => {
  const prods = listProducts.map(prd => ({
    itemId: prd.id,
    itemName: prd.name,
    price: prd.price,
    initialAvailableQuantity: prd.stock,
  }));
  res.json(prods);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const prd = getItemById(itemId);

  if (!prd) return res.json({ status: 'Product not found' });

  const rsvStock = await getCurrentReservedStockById(itemId);
  const currentQty = prd.stock - rsvStock;

  res.json({
    itemId: prd.id,
    itemName: prd.name,
    price: prd.price,
    initialAvailableQuantity: prd.stock,
    currentQuantity: currentQty,
  });
});

async function reserveStockById(itemId, stock) {
  await setCl(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getCl(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const prd = getItemById(itemId);

  if (!prd) return res.json({ status: 'Product not found' });

  if (prd.stock <= 0) return res.json({ status: 'Not enough stock available', itemId });

  await reserveStockById(itemId, prd.stock - 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen((port), (host), () => {
  console.log(`Server listening to ${host}/${port}`);
});
