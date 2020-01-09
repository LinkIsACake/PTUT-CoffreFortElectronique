'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    login: DataTypes.STRING,
    passwd: DataTypes.STRING
  }, {});
  User.associate = function(models) {
    // associations can be defined here
  };
  return User;
};

/*'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    login: {
			type:Sequelize.STRING,
			primaryKey: true,
			allowNull:false
		},
    passwd: {
			type:Sequelize.STRING,
			allowNull:false
		}
  }, {});
  User.associate = function(models) {
    // associations can be defined here
  };
  return User;
};
*/
