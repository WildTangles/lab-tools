# ruchardt-data-tool
Automate data capture for a typical [Rüchardt](https://en.wikipedia.org/wiki/R%C3%BCchardt_experiment#Experiment) setup.

Use [data_analysis.nb](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/data_analysis.nb) for data analysis and [tracker](https://github.com/OpenSourcePhysics/tracker) for data extraction.

The automation workflow makes use of [tracker](https://github.com/OpenSourcePhysics/tracker), Excel, and Mathematica. A video stream or a recorded video of the oscillating ball in the setup is also required for this to work. The workflow was originally used to reduce work and increase accuracy of heat capacity ratio calculations made during physics practical sessions at UCL.

Example Workflow:  
1. Record video/stream video of oscillating ball in the setup. An example recording is provided as [video_example.mp4](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/video_example.mp4).  
2. Extract the position-versus-time data of the oscillating ball from the video using [tracker](https://github.com/OpenSourcePhysics/tracker). The tracking session for the example recording is provided as [data_extraction.trk](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/data_extraction.trk).  
3. Export the tracking data. The exported data for the example recording is provided as [data_extraction.xlsx](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/data_extraction.xlsx).  
4. Strip the headers and extra information from exported data. Only the oscillating-coordinate position and time data is required. The stripped data for the example recording is provided as [raw_extracted_data.xlsx](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/raw_extracted_data.xlsx).  
5. Load the data into Mathematica. Fit a simple harmonic oscillator model to the tracking data to determine the frequency of oscillation. From this frequency, and measurements of the setup used, the heat capacity ratio can be derived. The model fitting for the example recording is provided as [data_analysis.nb](https://github.com/shrimpfriedrice/ruchardt-data-tool/blob/master/data_analysis.nb).
