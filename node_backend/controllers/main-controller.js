const express = require('express');
const decoder = new TextDecoder('utf-8');

exports.detectEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = req.body.time;
    const data = req.body.data;
    const windowSize = req.body.windowSize;
    const sd_th = req.body.sd_th;
    const pythonProcess = spawn('python3', [__dirname + '/python-files/event-detection.py', data, time, Number(windowSize), Number(sd_th)]);
    pythonProcess.stdout.on('data', (data) => {
        console.log(((decoder.decode(data))));
        const result = JSON.parse(decoder.decode(data));
        res.status(200).json(result);
    });
    pythonProcess.on('error', (error) => {
        console.error(`Python script error: ${error}`);
        res.status(500).json({ error: 'An error occurred' });
    });
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            console.log('Python script completed successfully.');
        } else {
            console.error(`Python script exited with code ${code}`);
            res.status(500).json({ error: 'An error occurred' });
        }
    });
});

exports.classifyEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = req.body.time;
    const data = req.body.data;
    const threshold_values = JSON.stringify(req.body.thresholdValues);
    const pythonProcess = spawn('python3', [__dirname + '/python-files/event-classification.py', data, time, threshold_values]);
    let responseData = "";
    pythonProcess.stdout.on('data', (data) => {
        data = decoder.decode(data);
        responseData += data;
    });
    pythonProcess.on('error', (error) => {
        console.error(`Python script error: ${error}`);
    });
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // console.log(result);
            const result = JSON.parse(JSON.parse(responseData));
            res.status(200).json(result);
        } else {
            console.error(`Python script exited with code ${code}`);
            // res.status(500).json({ error: 'An error occurred' });
        }
    });

})
exports.classifyIslandingEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = req.body.time;
    const datas = JSON.stringify(req.body.data);

    const threshold_values = JSON.stringify(req.body.thresholdValues);
    const pythonProcess = spawn('python3', [__dirname + '/python-files/event-classification-islanding.py', datas, time, threshold_values]);
    let responseData = "";
    pythonProcess.stdout.on('data', (data) => {
        data = decoder.decode(data);
        responseData += data;
        console.log(responseData);
    });
    pythonProcess.on('error', (error) => {
        console.error(`Python script error: ${error}`);
    });
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // console.log(result);
            const result = JSON.parse(responseData);
            res.status(200).json(result);
        } else {
            console.error(`Python script exited with code ${code}`);
            // res.status(500).json({ error: 'An error occurred' });
        }
    });

})
