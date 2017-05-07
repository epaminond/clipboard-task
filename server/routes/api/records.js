import Record from '../../models/Record';

export default (req, res) => {
  Record.find().then((records) => {
    res.json({
      records,
      success: true,
    });
  }).catch((error) => {
    res.json({
      error,
      success: false,
    });
  });
};
