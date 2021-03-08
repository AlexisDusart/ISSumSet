# ISSumSet: A Tweet Summarization Dataset Hidden in a TREC Track

This GitHub repository contains the code we used to transform the 2018-2019 TREC Incident Streams dataset into a tweet summarization dataset. You can find more information in the paper: "ISSumSet: A Tweet Summarization Dataset Hidden in a TREC Track".

## Parts of this repository

* [Model evaluation](./Model%20evaluation): Evaluate your own model
* [Paper annotations](./Paper%20annotations): Annotations (subevents, redundancy and coverage) 
* [Reproduce results](./Reproduce%20results): Reproduce results we reported in the paper, more detailed information about the analyses and examples
* [Sets](./Sets): Repository for sets/summaries (inluding **NHP** and **NHPAR** gold standards)
* [TREC IS annotations](./TREC%20IS%20annotations): TREC IS annotations
* [Tweets](./Tweets): Raw tweets

## Package Requirements

Python 3.7

```
easy-rouge==0.2.2
gensim==3.7.2
matplotlib==3.0.2
nltk==3.5
numpy==1.17.2
pandas==0.23.4
py-readability-metrics==1.4.3
scikit-learn==0.22.2.post1
scipy==1.2.1
seaborn==0.9.0
tqdm==4.28.1
```

* Run each python file in the directory of the file.

## Data Requirements

Download tweets and annotations on the TREC IS website :
* [Annotations](http://www.dcs.gla.ac.uk/~richardm/TREC_IS/2020/2020A/TRECIS_2018_2019-labels.json "TREC IS Annotations 2018-2019")
* [Tweets](http://dcs.gla.ac.uk/~richardm/TREC_IS/2020/data.html "TREC IS Tweets 2018-2019"): Follow the instructions and download **trecis2018-test**, **trecis2018-train**, **trecis2019-A-test** and **trecis2019-B-test** sets

* Put the annotations json file in the [TREC IS annotations](./TREC%20IS%20annotations) directory (See Section 3.2.1 of the paper)
* Put the tweets json files (unzip the IS files) in the [Tweets](./Tweets) directory (See Section 3.2.2 of the paper)

## First/Mandatory step

Run the python file :

```
python initialization.py [-remove_coverage=False]
```

* Summaries **NHP** and **NHPAR** will be generated and put into [Sets](./Sets) directory, see this [README](./Sets/README.md) for more details. (Section 5.3 of the paper)
* Using the option *-remove_coverage=True* you can genereate the **NHPAR** summaries without the coverage annotations. (Section 4.2.2 of the paper)

## Reproduce paper results

Once the initialization.py file has been run you can reproduce the results of the paper. To do so, see this [README.md](./Reproduce%20results/README.md) file.

## Evaluate your own model

You can compare your own model, see this [README](./Model%20evaluation/README.md) fore more details.

## Example

You can see below an example of summary with the summaries for the Chile Earthquake 2014 and Sandiego Synagogue Shooting 2019 events:

Chile earthquake: At least five dead as president declares northern disaster zone | ABC Radio Australia http://t.co/8cBlJVad1K  
@PatInDuhHat nope. - Tsunami warning in effect for Chile, Peru after magnitude 7.8 earthquake off northern Chile PTWC http://t.co/JtrD4z7vd3  
Earthquake 5 mb, 41 km WSW of Iquique, Chile | Earthquakes today http://t.co/MLtkJ5xdDC  
WA needs a seismic school retrofit program too. Another Warning for the Northwest From Chile’s Earthquake Hot Zone http://t.co/IqaMuVi7Py  
Chileans scramble for supplies after new quake - Yahoo News UK https://t.co/2bGk5fJf7l via @YahooNewsUK  
Chile's President Michelle Bachelet among evacuees as second earthquake hits video http://t.co/gu5IeBlKIJ http://t.co/qeZtS1pnfv #chile  
8.0 Earthquake Chile prompts Tsunami Evacuations and Chaos http://t.co/UDDd7ftTzo http://t.co/qeZtS1pnfv #chile  
Inmates escape after Chile earthquake http://t.co/lU1OD7kojJ



There was a shooting at a synagogue near San Diego this morning: https://t.co/IeMYboR5R4  
DEVELOPING: San Diego police have detained a man in connection with a possible shooting incident at the Chabad of Poway synagogue. https://t.co/WIrOBchI2m  
San Diego Synagogue Shooting: Multiple People Including Children Injured at Synagogue Chabad of Poway, Suspect in Custody https://t.co/zryDOMvTV3  
BREAKING: San Diego police said they have detained a man for questioning after there were reports of a shooter near a synagogue. There are multiple injuries. https://t.co/b3FzoxePpt  
Breaking: Multiple people gunned down at #Poway #California #synagogue shooting https://t.co/K84JDtr4Cz  
Another synagogue shooting, just 6 months after Pittsburgh. https://t.co/PDJw23lB5r  
Reports of several people shot at Poway synagogue https://t.co/afvxr6JfeI  
BREAKING: Authorities in Southern California say a shooting at a synagogue has left people injured but the extent is unclear. This is a developing story. https://t.co/ZNXpkKLzdZ  
The latest from the shooting at the Chabad of Poway synagogue: https://t.co/3CGWwFtx1v  
Live: San Diego Police hold press briefing on Poway synagogue shooting https://t.co/I5Rv8LEVgH via @YouTube  
1 Dead, Suspect Detained Following Synagogue Shooting in Poway https://t.co/32KxQIZ5Y1  
A man is in custody after a shooting at a San Diego-area synagogue on the last day of Passover that killed one and injured three, the town's mayor says https://t.co/2VRuzhFq6C https://t.co/95PahBJOHi

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

