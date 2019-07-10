%:- dynamic изменяет предикат во время его чтения, вставляет факт
/*
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
*/

% Review: Almost two hundred lines is quite a lot for Prolog.
% Consider separating definitions from axioms.
% Also delete the commented code.

%axiom 1 Reflexivity of Congruence
congruent(X, Y, Y, X).

congruent(X, Y, X, Y).
congruent(Y, Y, X, X).

% Review: Ahem. Why does you geometry include 14 axiomatic points?
congruent(a, b, a_, b_).
congruent(b, c, b_, c_).
congruent(a, c, a_, c_).

congruent(x, y, x_, y_).
congruent(x, u, x_, u_).
congruent(u, y, u_, y_).
congruent(y, z, y_, z_).
congruent(u, z, u_, z_).

isCongruent(A, B, C, D):-
			congruent(A, B, C, D);
			congruent(A, B, D, C);
			congruent(B, A, C, D);
			congruent(B, A, D, C), !.

laysBetween(a, y, x).
laysBetween(x, y, b).

laysBetweenLaw(A, B, C):-
			laysBetween(B, A, C);
			laysBetween(A, B, C).

%equality of triangles on three sides
equalityTriangles3(A, B, C, A_, B_, C_):-
					isCongruent(A, B, A_, B_),
					isCongruent(B, C, B_, C_),
					isCongruent(A, C, A_, C_), !.

isOnCircle(A, F, O):-
				isCongruent(A, O, F, O), !.

equalityArcs(A, B, C, D, F, O):-
			isOnCircle(A, F, O),
			isOnCircle(B, F, O),
			isOnCircle(C, F, O),
			isOnCircle(D, F, O),
				isCongruent(A, B, C, D), !.

%equality of angles
equalityAngles1(A, B, C, A_, B_, C_):-
		equalityTriangles3(A, B, C, A_, B_, C_), !.

% Review: An octary relation? Are there really that many points?
equalityAngles2(A, B, C, A_, B_, C_, F, O):-
		isOnCircle(A, F, O),
		isOnCircle(B, F, O),
		isOnCircle(C, F, O),
		isOnCircle(A_, F, O),
		isOnCircle(B_, F, O),
		isOnCircle(C_, F, O),
			equalityArcs(A, C, A_, C_, F, O), !.

equalityTriangles1(A, B, C, A_, B_, C_, F, O) :-
			isCongruent(A, B, A_, B_),
			isCongruent(C, B, C_, B_),
            equalityAngles2(A, B, C, A_, B_, C_, F, O), !.


% Review: I'm pretty sure you could write this as three separate rules.
equalityTriangles2(A, B, C, A_, B_, C_, F, O):-
		isCongruent(A, B, A_, B_),
				equalityAngles2(B, A, C, B_, A_, C_, F, O),
				equalityAngles2(A, B, C, A_, B_, C_, F, O), !;
		
		isCongruent(B, C, B_, C_),
				equalityAngles2(A, B, C, A_, B_, C_, F, O),
				equalityAngles2(A, C, B, A_, C_, B_, F, O), !;
		
		isCongruent(A, C, A_, C_),
				equalityAngles2(B, A, C, B_, A_, C_, F, O),
				equalityAngles2(A, C, B, A_, C_, B_, F, O), !.



intersectCircle(A, B, F, O):-
			circle(F, O),
			isInsideCircle(A, F, O),
			not(isInsideCircle(B, F, O));
			isInsideCircle(B, F, O),
			not(isInsideCircle(A, F, O)), !.

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
%axiom 2 Identity of Congruence
identityCongruence(X, Y):-
					isCongruent(X, Y, Z, Z), !.

%axiom 3 Transitivity of Congruence
transitivityCongruence(X, Y, Z, U, V, W):-
						isCongruent(X, Y, Z, U),
						isCongruent(X, Y, V, W),
						isCongruent(Z, U, V, W), !.

%axiom 4 Identity of Betweenness
identityBetweenness(X, Y):-
					laysBetweenLaw(X, X, Y), !.

%axiom 5 Axiom of Pasch
axiomPasch(U, Y, A, V, X):-
					laysBetweenLaw(U, Y, A),
					laysBetweenLaw(V, X, A),
					laysBetweenLaw(X, Z, U),
					laysBetweenLaw(Y, Z, V), !.

%axiom 6 Axiom schema of Continuity
schemaContinuity(A, B):-
				laysBetweenLaw(X, Y, B),
				laysBetweenLaw(A, Y, X).
/*
%axiom 7 Lower Dimension --we dont need this
lowerDimension():-
				laysBetweenLaw(A, B, C).
*/
%axiom 8 Upper Dimension
upperDimension(X, Y, Z):-
					laysBetweenLaw(X, Y, Z);
					laysBetweenLaw(X, Z, Y);
					laysBetweenLaw(Z, Y, X);
						isCongruent(X, U, X, V),
						isCongruent(Y, V, Y, U),
						isCongruent(Z, V, Z, U), !.

%axiom 9.1 Axiom of Euclid
axiomEuclid1(X, Y, Z):-
				laysBetweenLaw(X, Y, Z), !;
				laysBetweenLaw(Y, Z, X), !;
				laysBetweenLaw(Z, X, y), !;
					isCongruent(X, A, Y, A),
					isCongruent(X, A, Z, A), !.

%axiom 9.2 Axiom of Euclid
axiomEuclid2(X, Y, W, U, V, Z):-
				laysBetweenLaw(X, W, Y),
				laysBetweenLaw(X, V, U),
				laysBetweenLaw(W, V, Z),
					isCongruent(U, Y, V, Z),
					isCongruent(X, Y, Y, W),
					isCongruent(X, U, U, V),
					isCongruent(V, Z, Z, W), !.

%axiom 10 Five Segment
% Review: Five segment is considered to prove congruency between
% two given segments. The other eight should be found automatically.
fiveSegment(X, Y, U, Z, X_, Y_, U_, Z_):-	
				laysBetweenLaw(X, Z ,Y),
				laysBetweenLaw(X_, Z_, Y_),
					not(isCongruent(X, Y, P, P)),
					isCongruent(X, Y, X_, Y_),
					isCongruent(Y, Z, Y_, Z_),
					isCongruent(X, U, X_, U_),
					isCongruent(Y, U, Y_, U_),
					isCongruent(Z, U, Z_, U_), !.
