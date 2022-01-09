# Goal: Text conversion and entity recognition.

The goal is to grab all the of entities involved in the site investigation process. This will allow us to map the people, places, and organizations involved over time. This process is described below.

So far, we're using three substeps:
1. Convert PDF scans of SIR reports to text
2. Clean text
3. Run Spacy named entity recognition on text corpus

## First attempt
We began with a simple text conversion + Spacy pipeline. This didn't produce very good results. The text was messy (but largely usable) and many of the entities were mis-classified.

## Second attempt
After discussing the results of the first attempt, we decided to target our analysis more directly, by:
1. Selecting only SIR summary reports (large omnibus documents with executive summaries and a large collection of work from the SIR process)
2. Cleaning the text data more carefully - including the standard text cleaning tools (removing stopwords, etc); as well as document-specific operations (cropping, etc).
3. Re-running NER to see if we can produce more accurate results

Notes and results from step are described below. Note that outputs from each of the three steps are saved in their respective directories using the same filenames and folder structure as the PDF inputs. In other words: When you add documents to the "pdf_in" folder, the filenames and folder structure you use will set the tone for the rest of the outputs that you generate.

### 1. Document selection and text conversion
- Following our conversation, I grabbed summary report documents from the Drive repository. I manually cut these down to just the "executive summary" section, as we discussed. I added these to the 8 misc. documents in the "pdf_in" folder.
- These were converted to text using "1-sir2txt.py." Text files are saved in "txt_out"

### 2. Cleaning
- This step grabs texts from "txt_out", runs the basic cleaning tools described below using "2-clean_txt.py", and saves the results to "txt_clean".
- I first tried removing stopwords, lowercasing, removing punctuation, and removing hyperlinks and email addresses, but this didn't markedly improve NER. Then, the internet informed me that NER tools use these parts of the text to produce better output. This second attempt therefore only applies basic text cleaning: Removing newline characters to feed the full text as a single string, and removing multiple spaces. Ultimately, I opted not to remove links and emails - in one case, the NER tool identified an email address that consisted of someone's first and last names as a "person", which I thought might be a useful output.

### 3. Entity recognition
- This step uses "3-entity_recognition.py" to grab the texts from "txt_clean". It then runs an NER model to identify entities. Results are saved in "analysis_output": "nlp_output.spacy" includes the results of the NER model, saved as a Spacy "doc_bin" object (Git is set to ignore this large file). Entities and their tags are also saved under "analysis_output/entities_df": This folder contains one CSV file for each input document, saved using the same folder structure and filenames as the original PDF inputs.
- Previous attempts fed the data through Spacy's "en_core_web_lg" model. For this attempt, I switched over to the "en_core_web_trf" model (a transformer pipeline), as it's supposed to produce more accurate NER results. Transformers, as far as I understand, want GPU hardware - so even the short documents tested here taxed my GPU-less laptop pretty heavily. But the results are markedly better, I think.

### Reflection on second attempt
The executive summary sections of the SIR summary reports provide a lot of data. Classification results using TRF model seem, to me, pretty good. At this stage, here's what I see as the main challenges:

**Analyzing full summary reports, or focusing on the "executive summary" or introductory sections?** My guess is that the introductory sections of the SIR summary reports will contain all the major entities involved in the SIR process, meaning that it might work well for us to focus our attention on these sections. This is also a good idea because analyzing the full summary reports introduces two problems: reports include tables, maps, and other sections that don't easily translate to clean text; and the extremely long reports would require much more computing time than the 2-5 page introductions / exec summaries.

That said, extracting the introductory sections introduces a new problem. First, summary reports aren't uniform, so automating the extraction of intro sections would require some work (though that work may pay off down the road as an automated "SIR summary report section subsetter" tool). Subsetting summary reports manually seems doable, if it's just one report per site - but we don't end up with a nice "section subsetter" to show for it.


**Recombining addresses**: Most addresses are split into several separate entities: The street address; the city; and the state. Sometimes, the street address is listed as two entities: House number and street. If we want to extract and geolocate addresses, we'd need to recombine these separate elements into full addresses. I'm sure this can be done within the Spacy document object (eg: setting rules to extract sequential "LOCATION" and "GEOPOLITICAL ENTITY" tags).

**Dealing with duplicates**: Many entities are listed under multiple names (eg: "RIDEM" and "Rhode Island DEM"; "Warwick" and "the City of Warwick"). Depending on what kind of analysis we want to run, we may need to spend some time standardizing some of these outputs.

**TRF is computationally heavy,** but this is very solvable.
