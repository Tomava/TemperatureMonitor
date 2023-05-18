const express = require('express')
require('express-async-errors')
const app = express()
const cors = require('cors')

const dataRouter = require('./controllers/data')

app.use(cors())
app.use(express.json())
app.use('/api/data', dataRouter)

module.exports = app