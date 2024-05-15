const express = require('express');
const app = express();
const cors = require('cors');
const http = require('http');

const mainRouter = require('./routes/main-router');
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use('/v2',mainRouter);
app.use('/',(req,res,next)=>{
  res.status(200).json({ message: `Welcome`});
});
app.all('*', (req, res, next) => {
    next(new Error(`Can't find  ${req.originalUrl} on this server!`, 404));
  });
const port = 8080;


const server = http.createServer(app);
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
