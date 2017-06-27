#Water Treatment

Water treatment involves chlorinating the water via `chlorinator`.  It accepts
incoming connections on 1111 ("liquid"), and walks through the linked list.  It
will chlorinate (double-link) slightly less than 4% of the nodes.  "Slightly less"
because the final node can never be chlorinated.

#Sludge Treatment

The sludge processor, `sludger`, involves baking the solids for a long time.
Sludge treatment involves `scrypt`ing the string version of the data with the salt
"I Hate Liam Echlin".  It accepts liquid data on 4444, and outputs the sludge
form of that data downstream.


#Bugs/Concerns

* If too many solids come in at once, the sludger does not break them up into
separate packets.  Currently, only one comes in at a time from residential.

* Invalid packets are not retried.  This system should not log them, since any
packets this system receives would be internal from residential or pretreatment.

* Currently stormdrain is doing its own thing.  Might need to bring it in under
this control.

* Chlorination may dip too low if there are lots of tiny water packets.

* Not enough checking on input.
