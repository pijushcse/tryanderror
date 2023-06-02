import React, { useState } from 'react';
import headerImage from './header-image.jpg'; // Replace with the actual image file
import footerImage from './footer-image.jpg'; // Replace with the actual image file

const MyComponent = () => {
  const [year, setYear] = useState('');
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [results, setResults] = useState([]);

  const handleYearChange = (e) => {
    setYear(e.target.value);
  };

  const handleMakeChange = (e) => {
    setMake(e.target.value);
  };

  const handleModelChange = (e) => {
    setModel(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Make API call here with the provided values
    fetch(`http://localhost:8080/recalls?make=${make}&model=${model}&year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        setResults(data.results);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <header>
         <img src={headerImage} alt="Header" className="header-image" />
      </header>
      <form onSubmit={handleSubmit}>
	  <br />
        <label>
          Year:
          <select value={year} onChange={handleYearChange}>
            {Array.from({ length: 45 }, (_, i) => 1980 + i).map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </label>
        <br />
		<br />
        <label>
          Make:
          <input type="text" value={make} onChange={handleMakeChange} />
        </label>
        <br />
		<br />
        <label>
          Model:
          <input type="text" value={model} onChange={handleModelChange} />
        </label>
        <br />
		<br />
        <button type="submit">Submit</button>
      </form>
      <div>
        <h2>Results:</h2>
        <table>
          <thead>
            <tr>
              <th>Manufacturer</th>
              <th>NHTSA Campaign Number</th>
              <th>Report Received Date</th>
              <th>Component</th>
              <th>Summary</th>
              <th>Consequence</th>
              <th>Remedy</th>
              <th>Notes</th>
              <th>Model Year</th>
              <th>Make</th>
              <th>Model</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                <td>{result.manufacturer}</td>
                <td>{result.nHTSACampaignNumber}</td>
                <td>{result.reportReceivedDate}</td>
                <td>{result.component}</td>
                <td>{result.summary}</td>
                <td>{result.consequence}</td>
                <td>{result.remedy}</td>
                <td>{result.notes}</td>
                <td>{result.modelYear}</td>
                <td>{result.make}</td>
                <td>{result.model}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
	  <br />
	  <br />
	  <br />
	  <br />
	  <br />
	  <br />
      <footer>
        <img src={footerImage} alt="Header" className="footer-image" />
      </footer>
    </div>
  );
};

export default MyComponent;
