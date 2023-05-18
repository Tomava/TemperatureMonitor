const dataRouter = require('express').Router()
const csv = require('csv-parser')
const path = require('path');
const fs = require('fs');

dataRouter.get('/', async (request, response) => {
  const getFilenamesInDir = (dirPath) => {
    try {
      const filenames = fs.readdirSync(dirPath);
      return filenames;
    } catch (error) {
      console.error('Error reading directory:', error);
      return [];
    }
  };

  const directoryPath = `..${path.sep}data-fetching${path.sep}data`;
  const filenames = getFilenamesInDir(directoryPath);
  const filePaths = filenames.map((filename) => `${directoryPath}${path.sep}${filename}`)
  
  const readCSVFiles = (filePaths, prefix) => {
    const promises = filePaths.map((filePath) => {
      return new Promise((resolve, reject) => {
        if (String(filePath).search(prefix) !== -1) {
          const allData = [];
          fs.createReadStream(filePath)
            .pipe(csv({ separator: ';' }))
            .on('data', (data) => allData.push(data))
            .on('end', () => {
              resolve(allData);
            })
            .on('error', (error) => {
              reject(error);
            });
        } else {
          resolve([]); // Resolve with an empty array for non-matching prefixes
        }
      });
    });
  
    return Promise.all(promises)
      .then((fileDataArray) => fileDataArray.flat())
      .catch((error) => {
        console.error('Error reading CSV files:', error);
        return [];
      });
  };
  

  const InsideData = await readCSVFiles(filePaths, "inside")
  const OutsideData = await readCSVFiles(filePaths, "outside")

  response.json({InsideData: InsideData, OutsideData: OutsideData})
});

module.exports = dataRouter