%:- dynamic изменяет предикат во время его чтения, вставляет факт

permute(Pred, A, B) :-
	Perm1 =.. [Pred, A, B],
	assert(Perm1),
	Perm2 =.. [Pred, B, A],
	assert(Perm2).

permute(Pred, A, B, C) :-
	Perm1 =.. [Pred, A, B, C],
	assert(Perm1),
	Perm2 =.. [Pred, B, C, A],
	assert(Perm2).

%the first axiom Reflexivity of Congruence
congruent(X, Y, Y, X).

congruent(X, Y, X, Y).
congruent(Y, Y, X, X).

congruent(x, v, x, u).
congruent(y, v, y, u).
congruent(z, v, z, u).

laysBetween(u, y, a).
laysBetween(v, x, a).

laysBetween(z, x, y).
laysBetween(y, z, v).
/*
point(a).
point(b).
point(x).
point(y).
point(u).
point(z).
point(x_).
point(y_).
point(u_).
point(z_).
*/

%axioms
%the second axiom Identity of Congruence
identityCongruence(X, Y):-
					congruent(X, Y, Z, Z), !.

%the third axiom Transitivity of Congruence
transitivityCongruence(X, Y, Z, U, V, W):-
						congruent(X, Y, Z, U),
						congruent(X, Y, V, W),
						congruent(Z, U, V, W), !.

%the fourth axiom Identity of Betweenness
identityBetweenness(X, Y):-
					laysBetween(X, X, Y), !.

%the fifth axiom Axiom of Pasch
axiomPasch(U, Y, A, V, X):-
					laysBetween(U, Y, A),
					laysBetween(V, X, A),
					laysBetween(X, Z, U),
					laysBetween(Y, Z, V), !.

%the sixth axiom Axiom schema of Continuity --not works now
schemaContinuity():-
				laysBetween(A, Y, X),
				laysBetween(X, Y, B).

%the seventh axiom Lower Dimension --not works now
lowerDimention():-
				not(laysBetween(A, B, C)),
				not(laysBetween(B, C, A)),
				not(laysBetween(C, A, B)), !.

%the eighth axiom Upper Dimension
upperDimension(X, Y, Z):-
					laysBetween(X, Y, Z);
					laysBetween(X, Z, Y);
					laysBetween(Z, Y, X);
						congruent(X, U, X, V),
						congruent(Y, V, Y, U),
						congruent(Z, V, Z, U), !.

%the ninth axiom Axiom of Euclid
axiomEuclid(X, Y, Z):-
				laysBetween(X, Y, Z), !;
				laysBetween(Y, Z, X), !;
				laysBetween(Z, X, y), !;
					congruent(X, A, Y, A),
					congruent(X, A, Z, A), !.

fiveSegment(X, Y, U, Z, X_, Y_, U_, Z_):-	
/*				point(X),
				point(Y),
				point(U),
				point(Z),
				point(X_),
				point(Y_),
				point(U_),
				point(Z_),
*/					congruent(X, Y, X_, Y_),
						%not(I is 0), --dist betw X and Y needs to be fixed
					congruent(X, U, X_, U_),
					congruent(U, Y, U_, Y_),
					congruent(Y, Z, Y_, Z_),
					congruent(U, Z, U_, Z_), !.