E = csvread('example1.dat');

col1 = E(:,1);
col2 = E(:,2);
max_ids = max(max(col1,col2));
As= sparse(col1, col2, 1, max_ids, max_ids); 
A = full(As);

[v, D] = eig(A);

eigenvalues = sort(diag(D), 'descend');

