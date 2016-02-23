angular.module('chatApp', [])
    .factory('PostsService', ['$http', function($http) {
        return {
            getAllPosts: function(key, callback) {
                $http
                    .get('/all-posts',
                        {
                            params: {
                                'key': key
                            }
                        }
                    )
                    .then(function(response) {
                        return callback(response.data);
                    });
            },
            postPost: function(post, callback) {
                $http.post('/post-post', post).then(function(response) {
                    return callback(response);
                });
            }
        };
    }])
    .controller('PostsController', ['$scope', 'PostsService', '$interval',
        function($scope, PostsService, $interval) {
            $scope.posts = [];
            self.getAllPosts = function() {
                PostsService.getAllPosts($scope.key, function(data) {
                    console.log(data);
                    for (var i = 0; i < data.length; i++) {
                        $scope.posts[i] = data[i];
                    }                    
                });
            }
            $interval(self.getAllPosts, 100);
        }
    ])
    .controller('PostSubmitController', ['PostsService', 
        function(PostsService) {
            self = this;
            self.submit = function() {
                var post = {
                    username: self.username,
                    post: self.post
                };
                PostsService.postPost(post);
            };
            
        }
    ]);

