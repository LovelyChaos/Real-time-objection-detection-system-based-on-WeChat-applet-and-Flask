// pages/news/news.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    imglist : [],
    request_data:[],
  },
  
  

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  //强制刷新当前页面
  reloadThisPage() {
    let currentPages = getCurrentPages()
    let lastRoute = currentPages[currentPages.length - 1].route
    let options = currentPages[currentPages.length - 1].options
    let optionsStr = ""
    for (let key in options) {
        optionsStr += '?' + key + '=' + options[key]
    }
    wx.redirectTo({
        url: '/' + lastRoute + optionsStr,
    })
},

  img_w_show(){
    
    var _this=this; //var申明的变量是全局变量，其作用域为所在的函数内
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths;//图片的本地临时文件路径列表 (本地路径)

        var team_image = wx.getFileSystemManager().readFileSync(tempFilePaths[0], "base64") //将图片进行base64编码。图片的本地临时文件列表
        wx.request({
　　　　　　　　url: 'http://10.3.4.163:5000/predict',//API地址
　　　　　　　　header: {'content-type': "application/x-www-form-urlencoded",},
　　　　　　　　data: {image: team_image,},
               method: "POST",
　　　　　　　　success: function (reg) {
                
                _this.setData({
                imglist: tempFilePaths//_this.data.imglist.concat(
                })
                _this.setData({
                request_data: reg.data.resurl
                })
                console.log(reg.data)
　　　　　　　　}
　　　　　　　　})
        
      }
    })
  },
  
  
  


})