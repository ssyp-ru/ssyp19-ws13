permuteOrLays(Condition, A, B, C):-
			ABC =.. [Condition, A, B, C],
			BAC =.. [Condition, B, A, C],
			(call(ABC), !;
				call(BAC), !).
congruent(segment(a, b), segment(c, d)).

isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(A, B), segment(C, D)), !;
			congruent(segment(A, B), segment(D, C)), !;
			congruent(segment(B, A), segment(C, D)), !;
			congruent(segment(B, A), segment(D, C)), !;
			congruent(segment(C, D), segment(A, B)), !;
			congruent(segment(C, D), segment(B, A)), !;
			congruent(segment(D, C), segment(A, B)), !;
			congruent(segment(D, C), segment(B, A)), !.

laysBetweenLaw(A, B, C):-
			permuteOrLays(laysBetween, A, B, C).

identityCongruence(X, Y):-
			isCongruent(segment(X, Y), segment(Z, Z)), !.

transitivityCongruence(X, Y, Z, U, V, W):-
					isCongruent(segment(X, Y), segment(Z, U)),
					isCongruent(segment(X, Y), segment(V, W)),
					isCongruent(segment(Z, U), segment(V, W)), !.

identityBetweenness(X, Y):-
					laysBetweenLaw(X, X, Y), !.

axiomPasch(U, Y, A, V, X):-
					laysBetweenLaw(U, Y, A), laysBetweenLaw(V, X, A),
					laysBetweenLaw(X, Z, U), laysBetweenLaw(Y, Z, V), !.

upperDimension(X, Y, Z):-
				laysBetweenLaw(X, Y, Z);
				laysBetweenLaw(X, Z, Y);
				laysBetweenLaw(Z, Y, X);
					isCongruent(segment(X, U), segment(X, V)),
					isCongruent(segment(Y, V), segment(Y, U)),
					isCongruent(segment(Z, V), segment(Z, U)), !.

axiomEuclid1(X, Y, Z):-
				laysBetweenLaw(X, Y, Z), !;
				laysBetweenLaw(Y, Z, X), !;
				laysBetweenLaw(Z, X, Y), !;
					isCongruent(segment(X, A), segment(Y, A)),
					isCongruent(segment(X, A), segment(Z, A)), !.

axiomEuclid2(X, Y, W, U, V, Z):-
				laysBetweenLaw(X, W, Y),
				laysBetweenLaw(X, V, U),
				laysBetweenLaw(W, V, Z),
					isCongruent(segment(U, Y), segment(V, Z)), isCongruent(segment(X, Y), segment(Y, W)),
					isCongruent(segment(X, U), segment(U, V)), isCongruent(segment(V, Z), segment(Z, W)), !.

fiveSegment(U, Z, U_, Z_):-	
				laysBetweenLaw(X, Z ,Y),
				laysBetweenLaw(X_, Z_, Y_),
					isCongruent(segment(Z, U), segment(Z_, U_)),
					isCongruent(segment(X, Y), segment(X_, Y_)), isCongruent(segment(Y, Z), segment(Y_, Z_)),
					isCongruent(segment(X, U), segment(X_, U_)), isCongruent(segment(Y, U), segment(Y_, U_)), !.