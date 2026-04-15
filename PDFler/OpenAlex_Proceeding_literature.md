I am conducting a study on metadata quality in Library and Information Science
(LIS) journals published in Turkey. I plan to collect and compare metadata from
OpenAlex API and DergiPark API across six LIS journals.

Please find and summarize academic literature on:

metadata quality assessment in scholarly publishing evaluation frameworks, metrics, or indicators for metadata

quality (e.g., completeness, accuracy, consistency) studies using APIs (such as OpenAlex, Crossref, or similar) for

bibliometric or metadata analysis research specifically related to journal platforms like DergiPark or

regional/national indexing systems

Based on the literature, suggest possible research questions for a study focusing on comparing metadata quality

between two data sources (OpenAlex vs DergiPark) for the same set of journals.

Literature on metadata quality and data sources

The studies below provide both conceptual tools (how to think about “good” metadata) and concrete comparative

designs you can adapt to an OpenAlex–DergiPark study.

Metadata quality assessment in scholarly databases

Metadata quality is often operationalized as the amount, completeness, accuracy, and reliability of information
describing a publication, especially when records are aggregated from multiple sources (Delgado-Quirós & Ortega,

2024; C'espedes et al., 2024). Typical dimensions include:

•

Completeness: presence of key fields (title, authors, affiliations, abstract, keywords, references, funder,

identifiers) (Delgado-Quirós & Ortega, 2024; Alonso-Álvarez & Van Eck, 2024)- Accuracy/correctness:

agreement with a trusted source or manual validation (C'espedes et al., 2024; Alonso-Álvarez & Van Eck, 2024)-

Consistency/standardization: uniform formats and controlled identifiers (DOI, ORCID, funder IDs) and
consistent handling of document types, languages, and classifications (Delgado-Quirós & Ortega, 2024;

C'espedes et al., 2024; Culbert et al., 2024)- Richness/granularity: additional fields such as funding, licenses,

corrections, open access status, or peer-review metadata (Hendricks et al., 2020; Culbert et al., 2024; Alonso-

Álvarez & Van Eck, 2024)Comparative studies typically (a) define a sample of works, (b) extract records from
multiple databases, and (c) measure field‑level coverage and error rates (Delgado-Quirós & Ortega, 2024;
Culbert et al., 2024; Alonso-Álvarez & Van Eck, 2024; C'espedes et al., 2024).

Frameworks, metrics, and indicators

A recent comparison of eight free-access scholarly databases (including OpenAlex) uses a clear, transferable
framework: seven metadata categories (abstract, access, bibliographic info, document type, publication date,
language, identifiers) and two key metrics—field presence (coverage) and field completeness rate per record

(Delgado-Quirós & Ortega, 2024).

Other OpenAlex evaluations add:

•

Field‑specific accuracy via manual checking (e.g., language metadata) (C'espedes et al., 2024)- Per‑field
availability and correctness across multiple sources, distinguishing publication/author info vs. affiliations,
references, and funders (Alonso-Álvarez & Van Eck, 2024)- Journal‑level comparisons of ORCID coverage,
abstracts, and open‑access status across OpenAlex, Web of Science, and Scopus (Culbert et al., 2024)These
designs naturally generalize to LIS journals and to a pairwise comparison (OpenAlex vs. DergiPark).

1 / 5

Use of APIs for bibliometric/metadata analysis

APIs are now central to large‑scale scientometric work. A survey of 44 bibliographic APIs shows they are primarily
used for co‑authorship analysis, citation-based indicators, and metadata enrichment, with emphasis on identifier
interoperability (DOI, PubMedID, ORCID) (Velez-Estevez et al., 2023).

Specific tools and infrastructures:

•

OpenAlex metadata accessed via REST API and R packages (openalexR), with emphasis on coverage, citation

links, update speed, and openness (Aria et al., 2024)- Crossref, WoS, Scopus, Dimensions and others used via

APIs or data dumps for coverage, citation, and metadata quality studies (Hendricks et al., 2020; Baas et al.,

2020; Birkle et al., 2020; Visser et al., 2020; Mart'in-Mart'in et al., 2020)These works routinely compare

databases on coverage and metadata fields, providing templates for sampling, matching records, and handling

discrepancies.

OpenAlex and regional / non‑mainstream venues

Recent work stresses that OpenAlex has broader coverage than traditional proprietary databases but also notable

issues in metadata completeness and correctness, especially for fields such as abstracts, references, affiliations,

and funding (C'espedes et al., 2024; Culbert et al., 2024; Alonso-Álvarez & Van Eck, 2024; Chavarro et al., 2025).

For African journals, OpenAlex shows extensive coverage but lower completeness and accuracy for affiliations,

references, and funders, with better quality when journals are also in Scopus/WoS (Alonso-Álvarez & Van Eck,
2024).

A study on journals using Open Journal Systems (OJS) reveals that indexing in OpenAlex depends heavily on
Crossref DOIs; resource‑limited and non‑English journals remain under‑represented despite the inclusive design of
OpenAlex (Chavarro et al., 2025). This maps well onto questions about DergiPark, national indexing, and
Turkish‑language LIS journals.

DergiPark and national platforms

Direct, systematic metadata-quality evaluations of DergiPark were not found among the retrieved papers. However,
work on regional or thematic platforms (e.g., African Journals Online, OJS‑based journals) uses them as
comparison baselines for coverage and metadata completeness against large databases (Alonso-Álvarez & Van

Eck, 2024; Chavarro et al., 2025). This supports using DergiPark as the “local authoritative” source against which
OpenAlex is evaluated for your LIS journals.

Suggested research questions for an OpenAlex–DergiPark comparison

Drawing on these frameworks and methods (Delgado-Quirós & Ortega, 2024; C'espedes et al., 2024; Culbert et al.,

2024; Alonso-Álvarez & Van Eck, 2024; Chavarro et al., 2025), the following research questions fit a study of six

Turkish LIS journals:

1. Coverage and overlap

•

RQ1: For LIS journals hosted on DergiPark, what proportion of articles indexed in DergiPark are also indexed

in OpenAlex, and how does coverage vary by year and document type?

2. Field‑level completeness

2 / 5

•

•

RQ2: How do OpenAlex and DergiPark compare in the completeness of core descriptive metadata (title,

authors, affiliations, abstract, keywords, language, publication date, document type, volume/issue/pages) for

the same set of articles?

RQ3: Are there systematic differences in completeness of identifier-related fields (DOI, ISSN, ORCID,

funder identifiers) between OpenAlex and DergiPark?

3. Accuracy and consistency

•

•

RQ4: To what extent does metadata from OpenAlex and DergiPark agree with each other and with the

publisher/journal record on key fields (author list and order, affiliations, language, document type,

publication year)?

RQ5: Are there systematic patterns of metadata errors or inconsistencies (e.g., incorrect language

assignment, missing or mis-ordered authors, divergent document types) across the two sources?

4. Language and local visibility

•

RQ6: How accurately do OpenAlex and DergiPark record language and multilingual information for Turkish

LIS articles, and how might discrepancies affect bibliometric analyses of language use in the field (C'espedes

et al., 2024; Chavarro et al., 2025)?

5. Structural and infrastructural factors

•

RQ7: How do infrastructural characteristics—such as use of DOIs, registration with Crossref/DataCite, and
national indexing policies—relate to coverage, completeness, and accuracy of LIS journals in OpenAlex

relative to DergiPark (Hendricks et al., 2020; Alonso-Álvarez & Van Eck, 2024; Chavarro et al., 2025)?

6. Implications for bibliometric research

•

RQ8: How do differences in metadata quality between OpenAlex and DergiPark impact typical LIS

bibliometric indicators (e.g., publication counts, collaboration patterns, institutional mapping) computed for

these journals?

Possible structure for your empirical design

Comparative metadata dimensions for OpenAlex vs. DergiPark

Dimension

LIS/Turkey)

Citations

Typical indicators (adaptable to

Coverage

Share of DergiPark articles

(Delgado-Quirós & Ortega, 2024; Culbert et al.,

found in OpenAlex; overlap by
year/type

2024; Alonso-Álvarez & Van Eck, 2024; Chavarro
et al., 2025)

Descriptive
completeness

Presence of title, abstract,
keywords, language, doc type,

(Delgado-Quirós & Ortega, 2024; C'espedes et
al., 2024; Alonso-Álvarez & Van Eck, 2024)

pages

Contributor metadata

Authors, order, affiliations,
ORCID presence

(Culbert et al., 2024; Alonso-Álvarez & Van Eck,
2024; Chinchilla-Rodríguez et al., 2024)

3 / 5

Dimension

LIS/Turkey)

Citations

Typical indicators (adaptable to

Identifier richness

DOI, ISSN, funder IDs, other

(Hendricks et al., 2020; Delgado-Quirós &

persistent IDs

Ortega, 2024; Velez-Estevez et al., 2023; Alonso-
Álvarez & Van Eck, 2024)

Accuracy/consistency

Agreement between OpenAlex,
DergiPark, and journal webpage

(C'espedes et al., 2024; Culbert et al., 2024;
Alonso-Álvarez & Van Eck, 2024)

FIGURE 1  Main metadata dimensions and indicators for database comparison

These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at

https://consensus.app. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires

copyright holders’ consent.

References

Alonso-Álvarez, P., & Van Eck, N. (2024). Coverage and metadata completeness and accuracy of African research

publications in OpenAlex: A comparative analysis. Quantitative Science Studies. https://doi.org/10.1162/qss.a.396

Aria, M., Le, T., Cuccurullo, C., Belfiore, A., & Choe, J. (2024). openalexR: An R-Tool for Collecting Bibliometric Data

from OpenAlex. R J., 15, 167-180. https://doi.org/10.32614/rj-2023-089

Baas, J., Schotten, M., Plume, A., Côté, G., & Karimi, R. (2020). Scopus as a curated, high-quality bibliometric data

source for academic research in quantitative science studies. Quantitative Science Studies, 1, 377-386.

https://doi.org/10.1162/qss_a_00019

Birkle, C., Pendlebury, D., Schnell, J., & Adams, J. (2020). Web of Science as a data source for research on scientific

and scholarly activity. Quantitative Science Studies, 1, 363-376. https://doi.org/10.1162/qss_a_00018

C'espedes, L., Kozlowski, D., Pradier, C., Sainte-Marie, M., Shokida, N., Benz, P., Poitras, C., Ninkov, A., Ebrahimy,

S., Ayeni, P., Filali, S., Li, B., & Larivière, V. (2024). Evaluating the linguistic coverage of OpenAlex: An assessment of

metadata accuracy and completeness. Journal of the Association for Information Science and Technology, 76, 884

- 895. https://doi.org/10.1002/asi.24979

Chavarro, D., Alperin, J., & Willinsky, J. (2025). On the Open Road to Universal Indexing: OpenAlex and Open

Journal Systems. Quantitative Science Studies. https://doi.org/10.1162/qss.a.17

Chinchilla-Rodríguez, Z., Costas, R., Robinson-García, N., & Larivière, V. (2024). Examining the quality of the

corresponding authorship field in Web of Science and Scopus. Quantitative Science Studies, 5, 76-97.

https://doi.org/10.1162/qss_a_00288

Culbert, J., Hobert, A., Jahn, N., Haupka, N., Schmidt, M., Donner, P., & Mayr, P. (2024). Reference coverage

analysis of OpenAlex compared to Web of Science and Scopus. Scientometrics, 130, 2475 - 2492.

https://doi.org/10.1007/s11192-025-05293-3

Delgado-Quirós, L., & Ortega, J. (2024). Completeness degree of publication metadata in eight free-access

scholarly databases. Quantitative Science Studies, 5, 31-49. https://doi.org/10.1162/qss_a_00286

Hendricks, G., Tkaczyk, D., Lin, J., & Feeney, P. (2020). Crossref: The sustainable source of community-owned

scholarly metadata. Quantitative Science Studies, 1, 414-427. https://doi.org/10.1162/qss_a_00022

4 / 5

Mart'in-Mart'in, A., Thelwall, M., Orduña-Malea, E., & López-Cózar, E. (2020). Google Scholar, Microsoft

Academic, Scopus, Dimensions, Web of Science, and OpenCitations’ COCI: a multidisciplinary comparison of

coverage via citations. Scientometrics, 126, 871 - 906. https://doi.org/10.1007/s11192-020-03690-4

Velez-Estevez, A., Pérez, I., García-Sánchez, P., Moral-Munoz, J., & Cobo, M. (2023). New trends in bibliometric

APIs: A comparative analysis. Inf. Process. Manag., 60, 103385. https://doi.org/10.1016/j.ipm.2023.103385

Visser, M., Van Eck, N., & Waltman, L. (2020). Large-scale comparison of bibliographic data sources: Scopus, Web

of Science, Dimensions, Crossref, and Microsoft Academic. Quantitative Science Studies, 1-22.

https://doi.org/10.1162/qss_a_00112

5 / 5

