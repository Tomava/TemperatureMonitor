import React from 'react';
import LineGraph from './components/LineGraph';
import GraphData from './data/GraphData'

const App = () => {
  console.log(GraphData)
  return (
    <div>
      <h1>Temperature Data</h1>
      <LineGraph data={GraphData} />
    </div>
  );
};

export default App;
