permuteOrCongruence(Condition, A, C):-
			AC =.. [Condition, A, C],
			CA =.. [Condition, C, A],
			(call(AC), !; call(CA), !).

permuteAndTrianles(Condition, AB, BC, AC, AB_, BC_, AC_):-
			AB =.. [Condition, AB, AB_],
			BC =.. [Condition, BC, BC_],
			AC =.. [Condition, AC, AC_],
			call(AB), call(BC), call(AC), !.

permuteAndArcs(Condition, A, B, C, D, F, O):-
			A =.. [Condition, A, F, O],
			B =.. [Condition, B, F, O],
			C =.. [Condition, C, F, O],
			D =.. [Condition, D, F, O],
			call(A), call(B), call(C), call(D), !.

:-dynamic equalAngles/6.

equalAngles(A, B, C, A, B, C).

equalAngles(A, B, C, C, B, A).

congruent(segment(X, Y), segment(Y, X)).

congruent(segment(X, Y), segment(X, Y)).
congruent(segment(Y, Y), segment(X, X)).

isCongruent(segment(A, B), segment(C, D)):-
			permuteOrCongruence(congruent, segment(A, B), segment(C, D)), !.

laysBetweenLaw(A, B, C):-
			laysBetween(A, B, C), !;
			laysBetween(B, A, C), !.

equalityTriangles3(segment(A, B), segment(B, C), segment(A, C), segment(A_, B_), segment(B_, C_), segment(A_, C_)):-
		permuteAndTrianles(isCongruent, segment(A, B), segment(B, C), segment(A, C),
		segment(A_, B_), segment(B_, C_), segment(A_, C_)), !.

isOnCircle(segment(A, O), segment(F, O)):-
				isCongruent(segment(A, O), segment(F, O)), !.

equalityArcs(A, B, C, D, F, O):-
	permuteAndArcs(isOnCircle, A, B, C, D, F, O),
				isCongruent(segment(A, B), segment(C, D)), !.

equalityAngles1(A, B, C, A_, B_, C_):-
		equalityTriangles3(A, B, C, A_, B_, C_),
		assert(equalAngles(A, B, C, A_, B_, C_)), !.

equalityAnglesCircle(A, B, C, A_, B_, C_, F, O):-
		isOnCircle(B, F, O),
		isOnCircle(B_, F, O),
			equalityArcs(A, C, A_, C_, F, O),
				assert(equalAngles(A, B, C, A_, B_, C_)), !.

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
			(isInsideCircle(A, F, O),
				not(isInsideCircle(B, F, O)), !);
			(isInsideCircle(B, F, O),
				not(isInsideCircle(A, F, O)), !).