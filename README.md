# NYC-open-data-using-AWS-EC2-and-docker-

In this project we look to analyze data from the NYC Open Camera Parking Violations dataset that is available on NYC open data.
This dataset has 56.9 million rows and 19 columns. /n Each row is a record of a violation issued in New York city traced back from 2016 to now.
The columns include the violation type, the violation time, the fine amount, and the penalty amount,precint and plate among other violation details.

The main objective for this project is to be able to download atleast a 100,000 datapoints using socrata open data API, 
we will use amazon EC2 instance as a medium and write a python script that runs in docker to consume data
and then push it into an open search domain provisioned via AWS and draw insights from this data using kibana and create visuals to answer some basic qustions about the data.

<img width="1008" alt="avg_fine_amt_gauge" src="https://user-images.githubusercontent.com/42550664/201443509-a5f9483a-37f4-4484-92d7-e0fb1f4923c6.png">
<img width="1007" alt="bagofwords_issuing_agency" src="https://user-images.githubusercontent.com/42550664/201443517-4119e1ee-f8d7-472c-9082-0276cd0683d4.png">
