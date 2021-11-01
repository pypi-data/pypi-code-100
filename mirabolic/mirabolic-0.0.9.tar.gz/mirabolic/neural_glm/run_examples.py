# Sample code for performing a Poisson or Neg Binom regression using Keras

import generate_synthetic_data
import basic_glm_nn

# Probability distribution of observed counts
distribution_options = ['Poisson', 'Negative Binomial']
# Does exposure differ between observations?
exposure_options = [False, True]
# Make results repeatable
random_seed = 17
verbose = 0

for distribution in distribution_options:
    for exposure in exposure_options:
        print('\n')
        print(40*'#')
        print('##   %s %s' % (
            distribution, 'with exposure' if exposure else ''))
        print(40*'#')

        ##########################
        # Make some synthetic data
        ##########################
        synthesized = generate_synthetic_data.synthetic_data(
            N=100000,  # How many data points?
            distribution=distribution,
            exposure=exposure,
            random_seed=random_seed
        )
        features_split = synthesized.features_split
        labels_split = synthesized.labels_split

        ##########################
        # Make a neural net
        ##########################
        results = basic_glm_nn.build_and_train_basic_glm(
            loss=distribution,
            x_train=features_split['train'], y_train=labels_split['train'],
            x_test=features_split['test'], y_test=labels_split['test'],
            x_valid=features_split['valid'], y_valid=labels_split['valid'],
            exposure=exposure,
            random_seed=random_seed,
            verbose=verbose,
        )

        ##########################
        # Print results
        ##########################
        print('Betas:  True       Recovered')
        for i, key in enumerate(synthesized.true_betas):
            dash = 7*'='
            print('%s%s %s %s' % (7*' ', dash, key, dash))
            true_betas = synthesized.true_betas[key]
            recovered_betas = results['betas'][:, i]
            for i in range(len(true_betas)):
                true_beta = true_betas[i]
                recovered_beta = recovered_betas[i]
                print(7*' ', f'{true_beta:8.5f}',
                      ' ', f'{recovered_beta:8.5f}')
