const express = require('express');
const Router = express.Router();
const mainController = require('../controllers/main-controller');

Router.route('/detect-event')
    .post(mainController.detectEvent)
Router.route('/classify-event')
    .post(mainController.classifyEvent)
Router.route('/detect-islanding-event')
    .post(mainController.classifyIslandingEvent)
module.exports  = Router
