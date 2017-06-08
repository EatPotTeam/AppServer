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
        YOURAPPLICATION_SETTINGS: '/var/www/eatpotmovie-ci/config.py'
      }
    }
  ]
};
