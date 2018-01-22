/**
 * Created by cleiton on 31/12/2017 - 14:00.
 */
var application = angular.module('modules.configurations', ['angularUtils.directives.dirPagination','filters']);
application.controller('configurations_controller', function ($scope) {

	$scope.loaded_roms = false;
	$scope.load = function () {
	alert('VENHO AQUI???')
	}
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/roms/load_roms",

      success: function (data) {
        $scope.load_roms = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.loaded_roms = true;
        $scope.$apply();

      },

      failure: function () {
        $scope.loaded_roms = true;
        alert("Não foi possivel carregar a lista")
      }
    })
};
