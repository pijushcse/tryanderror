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
