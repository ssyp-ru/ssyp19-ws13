:-dynamic circle/2.
:-dynamic point/1.
:-dynamic laysBetween/3.
:-dynamic congruent/2.

laysBetweenLaw(X, X, X).

laysBetweenLaw(A, B, C) :-
	laysBetween(A, B, C).
laysBetweenLaw(A, B, C) :-
	laysBetween(B, A, C).

congruented(segment(A, B), segment(C, D)) :-
  congruent(segment(A, B), segment(C, D)).
congruented(segment(A, B), segment(C, D)) :-
  congruent(segment(A, B), X),
  congruented(X, segment(C, D)).

axiomEuclid2(segment(U, Y), segment(Z, A)) :-
				laysBetweenLaw(A, B, Y), congruented(segment(A, Y), segment(Y, B)),
				laysBetweenLaw(B, C, U), congruented(segment(B, U), segment(U, C)),
				laysBetweenLaw(C, A, Z), congruented(segment(C, Z), segment(Z, A)),
				assert(congruent(segment(U, Y), segment(Z, A))).

fiveSegment(segment(U, Z), segment(U_, Z_)):-
				laysBetweenLaw(X, Z ,Y),
				laysBetweenLaw(X_, Z_, Y_),
				congruented(segment(X, Y), segment(X_, Y_)),
				congruented(segment(Y, Z), segment(Y_, Z_)),
				congruented(segment(X, U), segment(X_, U_)),
				congruented(segment(Y, U), segment(Y_, U_)),
				assert(congruent(segment(Z, U), segment(Z_, U_))).

isCongruent(segment(A, B), segment(C, D)):-
		fiveSegment(segment(A, B), segment(C, D));
		axiomEuclid2(segment(A, B), segment(C, D));
		transit(segment(A, B), segment(C, D));
		congruented(segment(A, B), segment(C, D)).

identityCongruence(X, Y) :-
			congruented(segment(X, Y), segment(Z, Z)).
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
