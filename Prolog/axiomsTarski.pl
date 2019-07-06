%:- dynamic изменяет предикат во время его чтения, вставляет факт


/*downNote(A, B, C, J):-
				dist(A, B, F),
				dist(B, C, G),
				dist(A, C, K),
					J is 0,
					F is G + K;
					G is F + K;
					K is G + F,*/
dist(a, x, 1).
dist(a, y, 1).
dist(b, x, 2).
dist(b, y, 2).
dist(c, x, 4).
dist(c, y, 4).
dot(x).
dot(y).
dot(a).
dot(b).
dot(c).

%аксиомы
upperDimension(A, B, C, X, Y):-
				dot(X),
				dot(Y),
				dot(A),
				dot(B),
				dot(C),
				not(X = Y),
					dist(A, X, Q),
					dist(B, X, W),
					dist(C, X, E),
					dist(A, Y, R),
					dist(B, Y, T),
					dist(C, Y, U),
						Q is R,
						W is T,
						E is U, !.

fifthLength(X, Y, U, Z, X_, Y_, U_, Z_):-
					dist(X, Y, I),
						not(I is 0).
oneline(A, B, C):- upperDimension(A, B, C, M, N).