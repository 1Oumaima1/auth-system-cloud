const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Auth API OK' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Serveur port ' + PORT));
