const express = require('express');

const app = exress();

app.use(express.json());


app.post('/info', (req, res) => {
  const { name, email } = req.body;
  res.send(`Here is your json ${name} ${body}`)
})



app.listen(3000, () => {
  console.log('Running on port 3000')
})


