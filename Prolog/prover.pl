% display a proof tree
prove_p(A):-prove_p(A,P),write_proof(P).

% prove_p(A,P) <- P is proof tree of A
prove_p(true,[]):- !.
prove_p((A,B),[p((A,B),(A:-C))|Proof]):- !,
	clause(A,C),
	conj_append(C,B,D),
	prove_p(D,Proof).
prove_p(A,[p(A,(A:-B))|Proof]):-
	clause(A,B),
	prove_p(B,Proof).

write_proof([]):-
	write('...............[]'),nl.
write_proof([p(A,B)|Proof]):-
	write((:-A)),nl,
	write('.....|'),write('..........'),write(B),nl,
	write('.....|'),write('..................../'),nl,
	write_proof(Proof).

conj_append(true,Ys,Ys).
conj_append(X,Ys,(X,Ys)):-
    X \= true,
    X \= (_One, _TheOther).
conj_append((X,Xs),Ys,(X,Zs)):-
  conj_append(Xs,Ys,Zs).



