/* 
 * simple backend server for the web interface:
 * - handles requests from the web interface to create and manage games
*/

const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.listen(process.env.PORT || port, () => console.log(`Example app listening at http://localhost:${port}`));