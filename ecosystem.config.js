module.exports = {
  /**
   * Application configuration section
   * http://pm2.keymetrics.io/docs/usage/application-declaration/
   */
  apps : [

    // First application
    {
      name      : 'eatpotmovie-ci',
      script    : './deploy.sh',
      interpreter: '/bin/bash',
      env: {
        COMMON_VARIABLE: 'true'
      },
      // env_production : {
      //   NODE_ENV: 'production'
      // },
      env_dev : {
        API_APPKEY: 'gg',
        YOURAPPLICATION_SETTINGS: '/var/www/eatpotmovie-ci/config.py'
      }
    }
  ],

  /**
   * Deployment section
   * http://pm2.keymetrics.io/docs/usage/deployment/
   */
  deploy : {
    // production : {
    //   user : 'node',
    //   host : 'localhost',
    //   ref  : 'origin/master',
    //   repo : 'git@github.com:repo.git',
    //   path : '/var/www/production',
    //   'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production'
    // },
    dev : {
      user : 'www-data',
      host : 'localhost',
      ref  : 'master',
      repo : '.',
      path : '/var/www/blackhole-ci',
      'post-deploy' : 'npm install && pm2 startOrRestart ecosystem.config.js --env dev',
      env  : {
        NODE_ENV: 'dev'
      }
    }
  }
};
