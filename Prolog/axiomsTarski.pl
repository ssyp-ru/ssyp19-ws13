% display a proof tree
prove_p(A):-prove_p(A, P),write_proof(P).

% prove_p(A,P) <- P is proof tree of A
prove_p(true,[]):-!.

prove_p((A, B),[p((A, B), (A:-C))|Proof]):-!,
	clause(A, C),
	conj_append(C, B, D),
	prove_p(D, Proof).

prove_p(A, [p(A, (A:-B))|Proof]):-
	clause(A, B),
	prove_p(B, Proof).

write_proof([]):-
	write('...............[]'),nl.

write_proof([p(A, B)|Proof]):-
	write((:-A)),nl,
	write(B),nl,
	write_proof(Proof).

conj_append(true, Ys, Ys).
conj_append(X, Ys, (X, Ys)):-X\=true, X\=(_One, _TheOther).
conj_append((X, Xs), Ys, (X, Zs)):-conj_append(Xs, Ys, Zs).


laysBetween(u, y, a).
laysBetween(v, x, a).
laysBetween(x, z, u).
laysBetween(y, z, v).

congruent(segment(a, b), segment(c, d)).

congruent(segment(x, y), segment(z, u)).
congruent(segment(x, y), segment(v, w)).

isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), segment(C, D)), !.
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), segment(D, C)), !.
isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(B, A), segment(C, D)), !.
isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(B, A), segment(D, C)), !.
isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(C, D), segment(A, B)), !.
isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(C, D), segment(B, A)), !.
isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(D, C), segment(A, B)), !.
isCongruent(segment(A, B), segment(C, D)):-
			congruent(segment(D, C), segment(B, A)), !.

isCongruent(segment(A, B), segment(C, D)) :-
			congruent(segment(A, B), X),
			congruent(X, segment(C, D)), !.

laysBetweenLaw(A, B, C):-
			laysBetween(A, B, C), !;
			laysBetween(B, A, C), !.

identityCongruence(X, Y):-
			isCongruent(segment(X, Y), segment(Z, Z)), !.
/*
transitivityCongruence(Z, U, V, W):-
					isCongruent(segment(X, Y), segment(Z, U)),
					isCongruent(segment(X, Y), segment(V, W)), !.
*/
identityBetweenness(X, Y):-
					laysBetweenLaw(X, X, Y), !.

axiomPasch(U, Y, V, X):-
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