import { motion } from 'framer-motion';

const mockList = {
  title: 'Best Coffee Shops in OC',
  author: 'Alex Chen',
  avatar: 'AC',
  items: [
    { rank: 1, name: 'Portola Coffee Lab', location: 'Costa Mesa', rating: 4.8 },
    { rank: 2, name: 'Hidden House Coffee', location: 'San Juan Capistrano', rating: 4.7 },
    { rank: 3, name: 'Neat Coffee', location: 'Costa Mesa', rating: 4.6 },
    { rank: 4, name: 'Kean Coffee', location: 'Newport Beach', rating: 4.5 },
    { rank: 5, name: 'Daydream Surf Shop', location: 'Newport Beach', rating: 4.4 },
  ],
};

export default function ExamplePreview() {
  return (
    <section className="py-24 bg-amber-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            See it in action
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Beautiful ranked lists that are easy to create and share
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="flex justify-center"
        >
          <div className="w-full max-w-md">
            {/* Card */}
            <motion.div
              whileHover={{ y: -5 }}
              className="bg-white rounded-3xl shadow-2xl shadow-amber-200/50 overflow-hidden"
            >
              {/* Card header */}
              <div className="bg-gradient-to-r from-amber-500 to-orange-600 p-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-white/20 backdrop-blur rounded-full flex items-center justify-center text-white font-bold">
                    {mockList.avatar}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">{mockList.title}</h3>
                    <p className="text-amber-100">by {mockList.author}</p>
                  </div>
                </div>
              </div>

              {/* Card content */}
              <div className="p-4">
                {mockList.items.map((item, index) => (
                  <motion.div
                    key={item.name}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    whileHover={{ scale: 1.02, x: 5 }}
                    className="flex items-center gap-4 p-3 rounded-xl hover:bg-amber-50 transition-colors cursor-pointer"
                  >
                    {/* Rank badge */}
                    <div
                      className={`w-10 h-10 flex items-center justify-center rounded-full font-bold text-lg ${
                        item.rank === 1
                          ? 'bg-gradient-to-br from-amber-400 to-amber-600 text-white shadow-lg shadow-amber-400/40'
                          : item.rank === 2
                          ? 'bg-gradient-to-br from-gray-300 to-gray-400 text-white'
                          : item.rank === 3
                          ? 'bg-gradient-to-br from-amber-600 to-amber-800 text-white'
                          : 'bg-gray-100 text-gray-600'
                      }`}
                    >
                      {item.rank}
                    </div>

                    {/* Image placeholder */}
                    <div className="w-14 h-14 bg-gradient-to-br from-amber-100 to-orange-100 rounded-xl flex items-center justify-center">
                      <svg
                        className="w-6 h-6 text-amber-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                    </div>

                    {/* Info */}
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900">{item.name}</h4>
                      <p className="text-sm text-gray-500">{item.location}</p>
                    </div>

                    {/* Rating */}
                    <div className="flex items-center gap-1 text-amber-500">
                      <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                      </svg>
                      <span className="text-sm font-medium">{item.rating}</span>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Card footer */}
              <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() => console.log('Like clicked')}
                      className="flex items-center gap-1 hover:text-amber-600 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                        />
                      </svg>
                      <span>128</span>
                    </button>
                    <button
                      onClick={() => console.log('Comment clicked')}
                      className="flex items-center gap-1 hover:text-amber-600 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                        />
                      </svg>
                      <span>24</span>
                    </button>
                  </div>
                  <button
                    onClick={() => console.log('Share clicked')}
                    className="flex items-center gap-1 hover:text-amber-600 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                      />
                    </svg>
                    <span>Share</span>
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
