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



package com.example.demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.MapperFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
@RestController
@Slf4j
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    ObjectMapper mapper = new ObjectMapper();

    @PostConstruct
    public void init() {
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        mapper.configure(MapperFeature.ACCEPT_CASE_INSENSITIVE_PROPERTIES, true);
    }

    @CrossOrigin(origins = "*", allowedHeaders = "*")
    @GetMapping("/recalls")
    public @ResponseBody ApiResponse getRecalls(
            @RequestParam String make,
            @RequestParam String model,
            @RequestParam String year) {
        log.info("Received request for vehicle {} {} {}", year, make, model);
        String apiUrl = "https://api.nhtsa.gov/recalls/recallsByVehicle?make=" + make + "&model=" + model + "&modelYear=" + year;
        RestTemplate restTemplate = new RestTemplate();
        try {
            org.springframework.http.ResponseEntity<String> response = restTemplate.getForEntity(apiUrl, String.class, make, model, year);
            return mapper.readValue(response.getBody(), ApiResponse.class);
        } catch (Exception e) {
            ApiResponse r = new ApiResponse();
            r.setResults(new ArrayList<>());
            return r;
        }
    }

   private static class ApiResponse {
        private int count;
        private String message;
        private List<Result> results;

        public int getCount() {
            return count;
        }

        public void setCount(int count) {
            this.count = count;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public List<Result> getResults() {
            return results;
        }

        public void setResults(List<Result> results) {
            this.results = results;
        }
    }

	private static class Result {
        private String manufacturer;
        private String nHTSACampaignNumber;
        private boolean parkIt;
        private boolean parkOutSide;
        private String nHTSAActionNumber;
        private String reportReceivedDate;
        private String component;
        private String summary;
        private String consequence;
        private String remedy;
        private String notes;
        private String modelYear;
        private String make;
        private String model;

        public String getManufacturer() {
            return manufacturer;
        }

        public void setManufacturer(String manufacturer) {
            this.manufacturer = manufacturer;
        }

        public String getnHTSACampaignNumber() {
            return nHTSACampaignNumber;
        }

        public void setnHTSACampaignNumber(String nHTSACampaignNumber) {
            this.nHTSACampaignNumber = nHTSACampaignNumber;
        }

        public boolean isParkIt() {
            return parkIt;
        }

        public void setParkIt(boolean parkIt) {
            this.parkIt = parkIt;
        }

        public boolean isParkOutSide() {
            return parkOutSide;
        }

        public void setParkOutSide(boolean parkOutSide) {
            this.parkOutSide = parkOutSide;
        }

        public String getnHTSAActionNumber() {
            return nHTSAActionNumber;
        }

        public void setnHTSAActionNumber(String nHTSAActionNumber) {
            this.nHTSAActionNumber = nHTSAActionNumber;
        }

        public String getReportReceivedDate() {
            return reportReceivedDate;
        }

        public void setReportReceivedDate(String reportReceivedDate) {
            this.reportReceivedDate = reportReceivedDate;
        }

        public String getComponent() {
            return component;
        }

        public void setComponent(String component) {
            this.component = component;
        }

        public String getSummary() {
            return summary;
        }

        public void setSummary(String summary) {
            this.summary = summary;
        }

        public String getConsequence() {
            return consequence;
        }

        public void setConsequence(String consequence) {
            this.consequence = consequence;
        }

        public String getRemedy() {
            return remedy;
        }

        public void setRemedy(String remedy) {
            this.remedy = remedy;
        }

        public String getNotes() {
            return notes;
        }

        public void setNotes(String notes) {
            this.notes = notes;
        }

        public String getModelYear() {
            return modelYear;
        }

        public void setModelYear(String modelYear) {
            this.modelYear = modelYear;
        }

        public String getMake() {
            return make;
        }

        public void setMake(String make) {
            this.make = make;
        }

        public String getModel() {
            return model;
        }

        public void setModel(String model) {
            this.model = model;
        }
    }
}
