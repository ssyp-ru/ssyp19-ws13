%:- dynamic изменяет предикат во время его чтения, вставляет факт

permuteOrCongruence(Condition, A, C):-
			AC =.. [Condition, A, C],
			CA =.. [Condition, C, A],
			call(AC), !; call(CA), !.

permuteOrLays(Condition, A, B, C):-
			ABC =.. [Condition, A, B, C],
			BAC =.. [Condition, B, A, C],
			call(ABC), !; call(BAC), !.


permuteAnd(Condition, A, B, C):-
			ABC =.. [Condition, A, B, C],
			ACB =.. [Condition, A, C, B],
			BAC =.. [Condition, B, A, C],
			BCA =.. [Condition, B, C, A],
			CBA =.. [Condition, C, B, A],
			CAB =.. [Condition, C, A, B],
			call(ABC), call(ACB), call(BAC), call(BCA), call(CBA), call(CAB).

:-dynamic equalAngles/6.

equalAngles(A, B, C, A, B, C).

equalAngles(A, B, C, C, B, A).

%axiom 1 Reflexivity of Congruence
congruent(segment(X, Y), segment(Y, X)).

congruent(segment(X, Y), segment(X, Y)).
congruent(segment(Y, Y), segment(X, X)).

isCongruent(segment(A, B), segment(C, D)):-
			permuteOrCongruence(congruent, segment(A, B), segment(C, D)), !.

laysBetweenLaw(A, B, C):-
			permuteOrLays(laysBetween, A, B, C).
/*			laysBetween(B, A, C);
			laysBetween(A, B, C).*/

%equality of triangles on three sides
equalityTriangles3(A, B, C, A_, B_, C_):-
					isCongruent(segment(A, B), segment(A_, B_)),
					isCongruent(segment(B, C), segment(B_, C_)),
					isCongruent(segment(A, C), segment(A_, C_)), !.

isOnCircle(A, F, O):-
				isCongruent(segment(A, O), segment(F, O)), !.

equalityArcs(A, B, C, D, F, O):-
			isOnCircle(A, F, O),
			isOnCircle(B, F, O),
			isOnCircle(C, F, O),
			isOnCircle(D, F, O),
				isCongruent(segment(A, B), segment(C, D)), !.

%equality of angles
equalityAngles1(A, B, C, A_, B_, C_):-
		equalityTriangles3(A, B, C, A_, B_, C_),
		assert(equalAngles(A, B, C, A_, B_, C_)), !.


equalityAnglesCircle(A, B, C, A_, B_, C_, F, O):-
		isOnCircle(B, F, O),
		isOnCircle(B_, F, O),
			equalityArcs(A, C, A_, C_, F, O),
				assert(equalAngles(A, B, C, A_, B_, C_)), !.

%tops of angles expected in 1 point
equalityAnglesVertical(A, B, C, A_, B_, C_):-
			laysBetweenLaw(A, A_, B),
			laysBetweenLaw(C, C_, B),
				assert(equalAngles(A, B, C, A_, B_, C_)), !;

			laysBetweenLaw(A, C_, B),
			laysBetweenLaw(C, A_, B), 
				assert(equalAngles(A, B, C, A_, B_, C_)), !.

equalityTriangles1(A, B, C, A_, B_, C_):-
			isCongruent(segment(A, B), segment(A_, B_)),
			isCongruent(segment(B, C), segment(B_, C_)),
				equalAngles(A, B, C, A_, B_, C_), !.

equalityTriangles2(A, B, C, A_, B_, C_):-
		isCongruent(segment(A, B), segment(A_, B_)),
				equalAngles(A, B, C, A_, B_, C_),
				equalAngles(B, A, C, B_, A_,C_), !;
		
		isCongruent(segment(B, C), segment(B_, C_)),
				equalAngles(A, B, C, A_, B_, C_),
				equalAngles(B, C, A, B_, C_,A_), !;
		
		isCongruent(segment(A, C), segment(A_, C_)),
				equalAngles(B, A, C, B_, A_, C_),
				equalAngles(B, C, A, B_, C_, A_), !.

equalityTriangles(A, B, C, A_, B_, C_):-
			equalityTriangles1(A, B, C, A_, B_, C_), !;
			equalityTriangles2(A, B, C, A_, B_, C_), !;
			equalityTriangles3(A, B, C, A_, B_, C_), !.


intersectCircle(A, B, F, O):-
			circle(F, O),
			isInsideCircle(A, F, O),
			not(isInsideCircle(B, F, O));
			isInsideCircle(B, F, O),
			not(isInsideCircle(A, F, O)), !.

%axioms
%axiom 2 Identity of Congruence
identityCongruence(X, Y):-
					isCongruent(segment(X, Y), segment(Z, Z)), !.

%axiom 3 Transitivity of Congruence
transitivityCongruence(X, Y, Z, U, V, W):-
						isCongruent(segment(X, Y), segment(Z, U)),
						isCongruent(segment(X, Y), segment(V, W)),
						isCongruent(segment(Z, U), segment(V, W)), !.

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
						isCongruent(segment(X, U), segment(X, V)),
						isCongruent(segment(Y, V), segment(Y, U)),
						isCongruent(segment(Z, V), segment(Z, U)), !.



%axiom 9.1 Axiom of Euclid
axiomEuclid1(X, Y, Z):-
				laysBetweenLaw(X, Y, Z), !;
				laysBetweenLaw(Y, Z, X), !;
				laysBetweenLaw(Z, X, Y), !;
					isCongruent(segment(X, A), segment(Y, A)),
					isCongruent(segment(X, A), segment(Z, A)), !.

%axiom 9.2 Axiom of Euclid
axiomEuclid2(X, Y, W, U, V, Z):-
				laysBetweenLaw(X, W, Y),
				laysBetweenLaw(X, V, U),
				laysBetweenLaw(W, V, Z),
					isCongruent(segment(U, Y), segment(V, Z)),
					isCongruent(segment(X, Y), segment(Y, W)),
					isCongruent(segment(X, U), segment(U, V)),
					isCongruent(segment(V, Z), segment(Z, W)), !.

%axiom 10 Five Segment
fiveSegment(X, Y, U, Z, X_, Y_, U_, Z_):-	
				laysBetweenLaw(X, Z ,Y),
				laysBetweenLaw(X_, Z_, Y_),
					not(isCongruent(segment(X, Y), segment(P, P))),
					isCongruent(segment(X, Y), segment(X_, Y_)),
					isCongruent(segment(Y, Z), segment(Y_, Z_)),
					isCongruent(segment(X, U), segment(X_, U_)),
					isCongruent(segment(Y, U), segment(Y_, U_)),
					isCongruent(segment(Z, U), segment(Z_, U_)), !.