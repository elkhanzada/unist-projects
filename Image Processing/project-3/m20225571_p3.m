function m20225571_p3()
    clc; clear; close all;
    function compression()
        rgb_img = imread("k03.bmp");
        ycbcr_img = rgb2ycbcr(rgb_img);
        figure;
        imshow(ycbcr_img, []);
        axis off;
        yc = double(ycbcr_img(:, :, 1));
        [h, w] = size(yc);
        bck_size = 8;
        X_mat = [];
        
        for i = 1: bck_size : h
            for j = 1: bck_size: w
                bck = yc(i: i + bck_size - 1, j: j + bck_size -1);
                X_mat = [X_mat, bck(:)];
            end
        end
        fprintf("Size of X matrix: %d %d\n", size(X_mat))
        C_mat = X_mat * X_mat';
        fprintf("Size of C matrix: %d %d\n", size(C_mat))
        [V, D] = eig(C_mat);
        figure;
        plot(log10(diag(D)));
        xlabel("Eigen index");
        ylabel("Eigen value");
        title("Log10 of diag(D)");
        figure;
        plot(diag(V * V'));
        title("Orthonormal check");
        K = 64;
        [T_mat, D] = eigs(C_mat, K);
        fprintf("Size of T matrix: %d %d\n", size(T_mat));
        X_mat_repr = T_mat' * X_mat;
        mse = zeros(1, K);
        for k = 1 : K
            X_mat_pca = T_mat(:, 1:k) * X_mat_repr(1:k, :);
            mse(k) = mean(mean((X_mat - X_mat_pca).^2));
        end 
        figure;
        plot(1:K, mse);
        xlabel('K');
        ylabel('MSE');
        title('Mean Square Error vs K');
        
        reconstructed_images = [];
        figure;
        for i = 1:4
            pca = reshape(T_mat(:, i), bck_size, bck_size);
            subplot(1, 4, i);
            imagesc(pca);
            colormap gray;
            axis off;
            title(sprintf('Principal Component %d', i));
        
            X_mat_pca = T_mat(:, 1:i) * X_mat_repr(1:i, :);
            reconstructed_image_k = zeros(size(yc));
            idx = 1;
            for j = 1:bck_size:h
                for k = 1:bck_size:w
                    block_k = reshape(X_mat_pca(:, idx), bck_size, bck_size);
                    reconstructed_image_k(j:j+bck_size-1, k:k+bck_size-1) = block_k;
                    idx = idx + 1;
                end
            end
            reconstructed_images = [reconstructed_images, reconstructed_image_k(:)];
        end
        for i=1:4
            figure;
            imshow(reshape(reconstructed_images(:, i), size(yc)), []);
            colormap gray;
            axis off;
            title(sprintf('Reconstructed Image (K=%d)', i));
        end
    end
    function detection()
        figure;
        L = [];
        for i=1:20
            img = double(imread(sprintf("faces/%d.pgm", i)));
            [h, w] = size(img);
            L = [L, img(:)];
            subplot(4, 5, i);
            imshow(uint8(img));
            title(sprintf('Image %d', i));
        end
        fprintf("Size of L matrix: %d %d\n", size(L));
        Lbar = mean(L, 2);
        figure;
        imagesc(uint8(reshape(Lbar, [h,w])));
        colormap gray;
        axis off;
        title("Mean Image");
        L_centered = L - Lbar;
        C_mat = L_centered * L_centered';
        [V, D] = eigs(C_mat, 3);
        
        figure;
        for i = 1:3
            subplot(1, 3, i);
            imagesc(reshape(V(:, i), [h, w]));
            colormap gray;
            axis off;
            title(sprintf('Eigenface %d', i));
        end

        T_mat = [V(:, 1)'; V(:, 2)'; V(:, 3)'];
        x = T_mat * L_centered;
        fprintf("Size of x = %d %d\n", size(x));
        y = zeros([20,1]);
        y(1:10) = 1;
        y(10:20) = -1;
        figure;
        scatter3(x(1, :), x(2, :), x(3, :));
        title("Scatter plot of x data.")
        
        random_indices = randperm(10);
        random_indices = [random_indices(1:8), random_indices(1:8)+10];
        w = randn(size(x, 1), 1);
        b = rand();

        alpha = 0.001;
        
        epoch = 10;
        lambda = 1 / epoch;  
        
        fprintf("\nTRAINING...\n");
        for e = 1:epoch
            for i = 1:16
                % Randomly select a data point from the dataset
                random_idx = random_indices(i);
                x_sample = x(:, random_idx);
                y_sample = y(random_idx);
                prediction = 0;
                % Compute the gradients
                if (w' * x_sample + b) >= 1
                    prediction = 1;
                elseif (w' * x_sample + b) <= -1
                    prediction = -1;
                end
                if prediction == y_sample
                    dw = zeros(size(w));
                    db = 0;
                else
                    dw = -y_sample * x_sample;
                    db = -y_sample;
                end
                fprintf("Predicted = %d, Ground Truth = %d\n", prediction, y_sample);
                w = w - alpha * (dw + 2 * lambda * w);
                b = b - alpha * db;
            end
        end
        remaining = [];
        for i = 1:20
            if ismember(i, random_indices) == false
                remaining = [remaining, i];
            end
        end
        
        fprintf("\nTESTING...\n");
        for i = 1:size(remaining, 2)
            idx = remaining(i);
            x_sample = x(:, idx);
            y_sample = y(idx);
            if (w' * x_sample + b) >= 1
                prediction = 1;
            elseif (w' * x_sample + b) <= -1
                prediction = -1;
            end
            fprintf("Predicted = %d, Ground Truth = %d\n", prediction, y_sample);
        end
    end

    function image_estimate = restore_image(H, blurred, lambda)
         % Initialize the image estimate
        image_estimate = blurred(:);
        
        % Set the maximum number of iterations and the step size
        iteration = 0;
        step_size = 0.5;
        
        % Perform steepest descent optimization
        prev_value = Inf;
        patience = 0;
        while true
            gradient = 2 * (H' * H * image_estimate - H' * blurred(:)) + 2 * lambda * image_estimate;
            
            image_estimate = image_estimate - step_size * gradient;
            
            loss = norm(blurred(:) - H * image_estimate)^2 + lambda * norm(image_estimate)^2;
            
            if prev_value < loss
                patience = patience + 1;
            end
            if prev_value - loss < 1
                patience = patience + 1;
            else
                patience = 0;
            end    
            prev_value = loss;
            if patience > 3
                break;
            end
            iteration = iteration + 1;
            fprintf('Iteration: %d, Loss: %.2f\n', iteration, loss);
        end
    end
    function restoration()
        h = fspecial('gaussian', 7, 1);
        figure;
        imagesc(h/max(h(:))*255); colormap(gray(256)); axis off;
        M = 256;
        N = 256;
        K = 3;
        I = [];
        J = [];
        V = [];
        for i = 1:M
            for j = 1:N
                for m = -K:K
                    for n = -K:K
                        row_idx = mod(i - m - 1 + M, M) + 1;
                        col_idx = mod(j - n - 1 + N, N) + 1; 
                        linear_idx = (row_idx - 1) * N + col_idx;  
                        I = [I, (i - 1) * N + j];
                        J = [J, linear_idx];
                        V = [V, h(m + K + 1, n + K + 1)];
                    end
                end
            end
        end
        H = sparse(I, J, V);
        figure;
        spy(H);
        title("H matrix");


        img = double(imread('cman.tiff'));
        figure;
        subplot(2, 5, 1);
        imagesc(img);
        axis off;
        colormap gray;
        title('Original image')
        subplot(2, 5, 2);
        blurred = H * img(:);
        blurred = reshape(blurred, 256, 256);
        imagesc(blurred);
        axis off;
        colormap gray;
        title("Blurred image");
        
        image_estimate = restore_image(H, blurred, 0);
        restored_image = reshape(image_estimate, M, N);

        subplot(2,5,3);
        imagesc(restored_image);
        axis off;
        colormap gray;
        title('Restored Image (Without noise)');

        mse_org_res = mean(mean((img - restored_image).^2));
        mse_org_blur = mean(mean((img - blurred).^2));

        
        
        lambdas = [0, 1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1];
        results = zeros([length(lambdas), 5]);
        for idx = 1:length(lambdas)
            noisy_blurred = blurred + randn(size(blurred));
            image_estimate = restore_image(H, noisy_blurred, lambdas(idx));
            restored_image = reshape(image_estimate, M, N);
            subplot(2,5,idx+3);
            imagesc(restored_image);
            axis off;
            colormap gray;
            title(sprintf('Restored Image, Lambda = %.7f', lambdas(idx)));
            results(idx, 1) = lambdas(idx);
            results(idx, 2) = norm(noisy_blurred(:) - H * image_estimate)^2;
            results(idx, 3) = norm(image_estimate)^2;
            results(idx, 4) = mean(mean((img - restored_image).^2));
            results(idx, 5) = mean(mean((img - noisy_blurred).^2));
        end
        fprintf("No noise and Lambda is zero:\nMSE between original and restored: %.2f\n" + ...
            "MSE between original and blurred: %.2f\n", mse_org_res, mse_org_blur);
        for i = 1:length(lambdas)
            fprintf("Lambda = %.7f:\n", results(i, 1));
            fprintf("MSE between original and restored: %.2f\n" + ...
            "MSE between original and noisy blurred: %.2f\n", results(i, 4), results(i, 5));
        end
        figure;
        loglog(results(:, 2), results(:, 3));
        xlabel("||b-Ha||^2");
        ylabel("||a||^2");
        
    end
    
%compression();
%detection();
restoration();
end