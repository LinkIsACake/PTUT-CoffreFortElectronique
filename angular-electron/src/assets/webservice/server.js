const express = require('express');
const mime = require('mime');
const app = express();
const router = express.Router();

const cors = require('cors');
const fs = require('fs');


app.use(cors())

const dir = "../../../data"

router.get('/readFolder', (req, res) => {
  console.log("readFolder request")
  let filesList;

  if(!fs.existsSync(dir)){
    fs.mkdirSync(dir);
  }

  filesList = fs.readdirSync(dir);

  res.send(JSON.stringify(filesList))
});

router.get('/getFileInfo/:name',(req,res) => {
  const filename = req.url.split("/").pop();
  console.log("getFileInfo request for : " + filename);

  let fileStat = fs.statSync(dir + '/' + filename);
  res.send(JSON.stringify(fileStat))
});

router.get('/getFile/:name', (req,res) => {
    const filename = req.url.split("/").pop();
    console.log("getFile request for : " + filename);
    
  let file = dir + '/' + filename;
  let mimetype = mime.lookup(file);

  res.setHeader('Content-disposition', 'attachment; filename=' + filename);
  res.setHeader('Content-type', mimetype);
  
  let filestream = fs.createReadStream(file);
  // decrypt file
  filestream.pipe(res);
});

app.use(router)

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});
