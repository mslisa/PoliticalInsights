# PoliticalInsights

## Assignments
* Initial proposal: https://docs.google.com/document/d/1ZttaQalC6Si81o8bVNPymqfdY3DjCKr2_sSCF8Ytfeo/edit?usp=sharing
* Progress Report Week 4: https://docs.google.com/document/d/19y70UGbrxiNAH4ylYzBqs5Cg5TbUO97UKbrHVJ9cKXQ/edit#heading=h.vp5m1z6k4yhp
* Presentation Week 6: https://docs.google.com/presentation/d/1VvlkrU7ksasAXdBGLOyEc8xT_gFi4ZLmoJJh5K9s0vU/edit?usp=sharing
* Presentation Week 10:
* Presentation Final: 
* Notes: https://docs.google.com/document/d/1A6Spt8Dqo6v1g-rpkcFijOZNgdDY6Dlz8TDcKzJLQ78/edit

## Resources

### Data sets

* Public information and social media presences data: http://docs.everypolitician.org/data_summary.html
* Voter pamphlets: http://repository.uchastings.edu/ca_ballot_props/1343/ 
* TV Commercials: http://www.livingroomcandidate.org/ 
* GovTrack: https://www.govtrack.us/congress/members/suzanne_bonamici/412501 
* Countable: https://www.countable.us/about/us 
* MLB stat scorecard (as an idea for presentation): http://m.mlb.com/player/514888/jose-altuve?year=2017&stats=bvp-r-hitting-mlb

### Code and Programming

* Starspace, a general-purpose neural model for efficient learning of entity embeddings: https://github.com/facebookresearch/Starspace
* When working with virtualenv, Windows users should do two things:
  * need to fix how python is called. Either enter <code>alias python='winpty python.exe</code> every time OR
  * for a more permenant solution, update your .bashrc
    * <code>cd ~</code>
    * <code>vim .bashrc</code>
    * in .bashrc add the <code>alias</code> statement from above

## Timeline

* Weekly assignments doc: https://docs.google.com/document/d/1sq3Vj2XlGutVVCF3X525YBhhTFJkKFzIJVjs1Vpym2M/edit

## Questions and Issues (MoSCoW)

### Overall
* C - Where did the contact information per rep go?
* C - Graphs scalable to phone? They're running off the page; is there a dynamic setting?
* C - Can we make graph points "jump" to new position?
* C -Can we add data tables below graphs with the selected rep's numbers?

### Top of page
* S - Make address bar constant so you can switch addresses.
* S - Can we add a button to submit for address? Mom didn't think to push return/enter to submit.
* C - Can we make images buttons to impact rest of form?

### Effectiveness
* C - Can we set score as 1 - [score]/100 or something? The large number at [0,0] was confusing.
* C - Hoverover grey on grey was hard to read.
* C - Hoverover grey box could use more of a boarder so it's not so tight on cursor.
* S - For HOR graph, those vertical bars that pop up drew questions. Can we include a quick analysis blurb to explain *if* the house of representative rep is selected?

### Bipartisan
* C - The bullets were skipped since they were assumed to be the same as prior graph. Drew some confusions on the graph until user realized to read the bullets. Not sure if there's a way to fix this? Maybe make the whole this less word heavy?
* C - The lack of hover for this graph was interpreted as something was broken.
* S - The line isn't at the same place per bar and covers the number sometimes.

### Finance
* M - No title or y-axis numbers/major ticks.
* C - Rep names are now capitalized and were camel case in prior graphs. Do we just fix in data?
* C - Hoverover grey box could use more of a boarder so it's not so tight on cursor.
* C - Have the comment on no data for the person only show up if there isn't data for the person?
