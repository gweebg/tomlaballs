const express = require('express');
const Tomlaballs = require('../controllers/tomlaballs');

const router = express.Router();


router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

module.exports = router;
