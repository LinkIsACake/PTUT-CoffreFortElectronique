const express = require('express');
const app = express();

const cors = require('cors');
const fs = require('fs');


app.use(cors())

app.get('/', (req, res) => {
  let filesList;

  filesList = fs.readdirSync("./");

  console.log(filesList)
  res.send(JSON.stringify(filesList))
});

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});
