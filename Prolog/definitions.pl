:-consult(axiomsTarski).
:-dynamic equalAngles/6.

equalAngles(A, B, C, A, B, C).

equalAngles(A, B, C, C, B, A).

equalityTriangles3(segment(A, B), segment(B, C), segment(A, C),
				   segment(A_, B_), segment(B_, C_), segment(A_, C_)):-
		isCongruent(segment(A, B), segment(A_, B_)),
		isCongruent(segment(B, C), segment(B_, C_)),
		isCongruent(segment(A, C), segment(A_, C_)), !.

isOnCircle(segment(A, O), F):-
				isCongruent(segment(A, O), segment(O, F)), !.

equalityArcs(A, B, C, D, F, O):-
				isOnCircle(segment(A, O), F),
				isOnCircle(segment(B, O), F),
				isOnCircle(segment(C, O), F),
				isOnCircle(segment(D, O), F),
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
			laysBetween(A, A_, B),
			laysBetween(C, C_, B),
				assert(equalAngles(A, B, C, A_, B_, C_)), !;

			laysBetween(A, C_, B),
			laysBetween(C, A_, B), 
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