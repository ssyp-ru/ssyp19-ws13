prove_p(A) :-prove_p(A, P),write_proof(P).
prove_p(true,[]).

prove_p((A, B),[p((A, B), (A:-C))|Proof]) :-
	clause(A, C),
	conj_append(C, B, D),
	prove_p(D, Proof).

prove_p(A, [p(A, (A:-B))|Proof]) :-
	clause(A, B),
	prove_p(B, Proof).

write_proof([]) :-
	write('...............[]'), nl.

write_proof([p(A, B)|Proof]) :-
	write((:-A)),nl,
	write(B),nl,
	write_proof(Proof).

conj_append(true, Ys, Ys).
conj_append(X, Ys, (X, Ys)) :-X\=true, X\=(_One, _TheOther).
conj_append((X, Xs), Ys, (X, Zs)) :-conj_append(Xs, Ys, Zs).

:-dynamic circle/2.
:-dynamic point/1.
:-dynamic laysBetween/3.
:-dynamic congruent/2.

isCongruent(segment(A, B), segment(A, B)).
isCongruent(segment(A, B), segment(B, A)).
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(B, A), segment(C, D)).
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), segment(C, D)).
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(B, A), segment(D, C)).
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), segment(D, C)).
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), X),
			isCongruent(X, segment(C, D)).
%Euclid's Axiom: midline is equal to half of parallel edge
isCongruent(segment(U, Y), segment(Z, A)) :-
				laysBetweenLaw(A, B, Y), isCongruent(segment(A, Y), segment(Y, B)),
				laysBetweenLaw(B, C, U), isCongruent(segment(B, U), segment(U, C)),
				laysBetweenLaw(C, A, Z), isCongruent(segment(C, Z), segment(Z, A)).
%fiveSegment
isCongruent(segment(U, Z), segment(U_, Z_)):-
				laysBetweenLaw(X, Z ,Y),
				laysBetweenLaw(X_, Z_, Y_),
					isCongruent(segment(Z, U), segment(Z_, U_)),
					isCongruent(segment(X, Y), segment(X_, Y_)), isCongruent(segment(Y, Z), segment(Y_, Z_)),
					isCongruent(segment(X, U), segment(X_, U_)), isCongruent(segment(Y, U), segment(Y_, U_)).
laysBetweenLaw(A, B, C) :-
	laysBetween(A, B, C).
laysBetweenLaw(A, B, C) :-
	laysBetween(B, A, C).

laysBetweenLaw(X, X, Y) :- Y is X.

oneLine(A, B, C) :-
	laysBetweenLaw(A, B, C).
oneLine(A, B, C) :-
	laysBetweenLaw(B, C, A).
oneLine(A, B, C):-
	laysBetweenLaw(A, C, B).

identityCongruence(X, Y) :-
			isCongruent(segment(X, Y), segment(Z, Z)).
identityBetweenness(X, Y) :-
					laysBetweenLaw(X, X, Y).
axiomPasch(U, Y, V, X) :-
					laysBetweenLaw(U, Y, A), laysBetweenLaw(V, X, A),
					laysBetweenLaw(X, Z, U), laysBetweenLaw(Y, Z, V).
upperDimension(X, Y, Z) :-
					isCongruent(segment(X, U), segment(X, V)),
					isCongruent(segment(Y, V), segment(Y, U)),
					isCongruent(segment(Z, V), segment(Z, U)).
axiomEuclid1(X, Y, Z):-
				not(oneLine(X, Y, Z)),
					isCongruent(segment(X, A), segment(Y, A)),
					isCongruent(segment(X, A), segment(Z, A)).