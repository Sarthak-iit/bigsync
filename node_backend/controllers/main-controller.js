const express = require('express');
const decoder = new TextDecoder('utf-8');
const fs = require('fs');
const os = require('os');
const path = require('path');
const dotenv = require('dotenv');
dotenv.config({ path: './../node_backend/config.env' });
const script = process.env.SCRIPT;

exports.detectEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = (req.body.time);
    const data = (req.body.data);
    const windowSize = req.body.windowSize;
    const sd_th = req.body.sd_th;


    // 
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'myapp-'));
    const dataFilePath = path.join(tempDir, 'data.json');
    fs.writeFileSync(dataFilePath, JSON.stringify([data,time]));
    // 
    const pythonProcess = spawn(script, [__dirname + '/python-files/event-detection.py', dataFilePath,Number(windowSize), Number(sd_th)]);
    pythonProcess.stdout.on('data', (data) => {
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
            res.status(500).json({ error: `An error occurred with code ${code}`});
        }
    });
});


exports.classifyEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = req.body.time;
    const data = req.body.data;
    const threshold_values = JSON.stringify(req.body.thresholdValues);
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'myapp-'));
    const dataFilePath = path.join(tempDir, 'data.json');
    fs.writeFileSync(dataFilePath, JSON.stringify([data,time]));
    const pythonProcess = spawn(script, [__dirname + '/python-files/event-classification.py', dataFilePath, threshold_values]);
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
            res.status(500).json({ error: `An error occurred with code ${code}`});
        }
    });

})
exports.classifyIslandingEvent = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    const time = req.body.time;
    const data = req.body.data;
    const threshold_values = JSON.stringify(req.body.thresholdValues);

    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'myapp-'));
    // console.log(tempDir)
    const dataFilePath = path.join(tempDir, 'data.json');
    fs.writeFileSync(dataFilePath, JSON.stringify([data,time]));
    const pythonProcess = spawn(script, [__dirname + '/python-files/event-classification-islanding.py', dataFilePath, threshold_values]);
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
            res.status(500).json({ error: `An error occurred with code ${code}`});
        }
    });
})
exports.findStatistics = ((req, res, next) => {
    const spawn = require('child_process').spawn;
    let data = JSON.stringify(req.body.data);
    // 
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'myapp-'));
    const dataFilePath = path.join(tempDir, 'data.json');
    fs.writeFileSync(dataFilePath,data);
    // 
    const pythonProcess = spawn(script, [__dirname + '/python-files/baselining.py', dataFilePath]);
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
            res.status(500).json({ error: `An error occurred with code ${code}`});
        }
    });
})