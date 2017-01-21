docker run --name gitlab-postgresql -d \
    --env 'DB_NAME=gitlabhq_production' \
    --env 'DB_USER=gitlab' --env 'DB_PASS=password' \
    --env 'DB_EXTENSION=pg_trgm' \
    sameersbn/postgresql:9.5-3
#    --volume /srv/docker/gitlab/postgresql:/var/lib/postgresql \

docker run --name gitlab-redis -d \
    sameersbn/redis:latest
    #--volume /srv/docker/gitlab/redis:/var/lib/redis \


docker run --name gitlab -d \
    --link gitlab-postgresql:postgresql --link gitlab-redis:redisio \
    --publish 10022:22 --publish 2333:80 \
    --env 'GITLAB_PORT=10080' --env 'GITLAB_SSH_PORT=10022' \
    --env 'GITLAB_HOST=localhost' \
    --env 'GITLAB_SECRETS_DB_KEY_BASE=long-and-random-alpha-numeric-string' \
    --env 'GITLAB_SECRETS_SECRET_KEY_BASE=long-and-random-alpha-numeric-string' \
    --env 'GITLAB_SECRETS_OTP_KEY_BASE=long-and-random-alpha-numeric-string' \
    sameersbn/gitlab:8.14.4
#    --volume /srv/docker/gitlab/gitlab:/home/git/data \
