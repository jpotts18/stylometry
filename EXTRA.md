# Stylometry

This is a script based on a paper called [Using Machine Learning Techniques for Stylometry](http://www2.tcs.ifi.lmu.de/~ramyaa/publications/stylometry.pdf)

The purpose of this python library is to perform NLP to identify authorship.

The main features that are analyzed in this library are:

1. type-token ratio: The type-token ratio indicates the richness of an author’s vocabulary. The higher the ratio, the more varied the vocabulary. It also reflects an author’s tendency to repeat words.

2. mean word length: Longer words are traditionally associated with more pedantic and formal styles, whereas shorter words are a typical feature of informal spoken language.

3. mean sentence length: Longer sentences are often the indicator of carefully planned writing, while shorter sentences are more characteristic of spoken language.

4. standard deviation of sentence length: The standard deviation indicates the variation of sentence length, which is an important marker of style.

5. mean paragraph length: The paragraph length is much influenced by the occurrence of dialogues.

6. chapter length: The length of the sample chapter.

7. number of commas per thousand tokens: Commas signal the ongoing flow of ideas within a sentence.

8. number of semicolons per thousand tokens: Semicolons indicate the reluctance of an author to stop a sentence where (s)he could.

9. number of quotation marks per thousand tokens: Frequent use of quotations is considered a typical involvement-feature.

10. number of exclamation marks per thousand tokens: Exclamations signal strong emotions.In fact, many previous research included Austen and the Brontë sisters because of their similarity. Mean sentence length has been considered by some as unreliable, and the frequency distributions of the logarithms of sentence length have been used as well.

11. number of hyphens per thousand tokens: Some authors use hyphenated words more than others.

12. number of ands per thousand tokens: Ands are markers of coordination, which, as opposed to subordination, is more frequent in spoken production.

13. number of buts per thousand tokens: The contrastive linking buts are markers of coordination too.

14. number of howevers per thousand tokens: The conjunct “however” is meant to form a contrastive pair with “but”.

15. number of ifs per thousand tokens: If-clauses are samples of subordination.

16. number of thats per thousand tokens: Most of the thats are used for subordination while a few are used as demonstratives.

17. number of mores per thousand tokens: ‘More’ is an indicator of an author’s preference for comparative structure.

18. number of musts per thousand tokens: Modal verbs are potential candidates for expressing tentativeness. Musts are more often used non-epistemically.

19. number of mights per thousand tokens: Mights are more often used epistemically.

20. number of thiss per thousand tokens: Thiss are typically used for anaphoric reference.

21. number of verys per thousand tokens: Verys are stylistically significant for its emphasis on its modifiees.


